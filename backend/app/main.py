from __future__ import annotations
import uuid
import structlog
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import Base, engine
from app.routers import auth, health, menu, category, order, sse, table, message

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.BoundLogger,
    logger_factory=structlog.PrintLoggerFactory(),
)
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    import os
    os.makedirs(settings.upload_dir, exist_ok=True)
    Base.metadata.create_all(bind=engine)

    # Initialize OpenTelemetry
    from app.telemetry import init_telemetry
    init_telemetry()

    # Auto-instrument FastAPI and SQLAlchemy
    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
        FastAPIInstrumentor.instrument_app(app)
        SQLAlchemyInstrumentor().instrument(engine=engine)
    except Exception:
        pass  # OTel not available in test env

    yield


app = FastAPI(title="Table Order API", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for uploads
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# Routers
app.include_router(health.router)
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(category.router, prefix="/api/categories", tags=["categories"])
app.include_router(menu.router, prefix="/api/menus", tags=["menus"])
app.include_router(order.router, prefix="/api/orders", tags=["orders"])
app.include_router(table.router, prefix="/api/tables", tags=["tables"])
app.include_router(sse.router, prefix="/api/sse", tags=["sse"])
app.include_router(message.router, prefix="/api/messages", tags=["messages"])



# HTTP metrics middleware
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    import time as _time
    try:
        from app.telemetry import http_request_count, http_request_duration, http_active_requests
        route = request.url.path
        method = request.method
        attrs = {"http_route": route, "http_request_method": method}
        http_active_requests.add(1, attrs)
        start = _time.perf_counter()
        response = await call_next(request)
        duration = _time.perf_counter() - start
        attrs["http_response_status_code"] = str(response.status_code)
        http_request_count.add(1, attrs)
        http_request_duration.record(duration, attrs)
        http_active_requests.add(-1, {"http_route": route, "http_request_method": method})
        return response
    except Exception:
        return await call_next(request)


# Security headers middleware
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    if request.url.path in ("/docs", "/redoc", "/docs/oauth2-redirect"):
        response.headers["Content-Security-Policy"] = "default-src 'self' https://cdn.jsdelivr.net https://fastapi.tiangolo.com 'unsafe-inline'"
    else:
        response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


# Request ID middleware
@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("unhandled_exception", error=str(exc), path=request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
