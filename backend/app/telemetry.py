from __future__ import annotations
import os
import time

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

_initialized = False

meter: metrics.Meter = metrics.get_meter("table-order")

# Custom metrics
orders_created = meter.create_counter("orders_created", unit="1", description="Total orders created")
sse_connections = meter.create_up_down_counter("sse_active_connections", unit="1", description="Active SSE connections")
recommendations_generated = meter.create_counter("recommendations_generated", unit="1", description="Total recommendations generated")

# HTTP metrics
http_request_count = meter.create_counter("http_server_requests", unit="1", description="Total HTTP requests")
http_request_duration = meter.create_histogram("http_server_request_duration_seconds", unit="s", description="HTTP request duration")
http_active_requests = meter.create_up_down_counter("http_server_active_requests", unit="1", description="Active HTTP requests")


def init_telemetry():
    global _initialized
    if _initialized:
        return
    _initialized = True

    endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    if not endpoint:
        return

    resource = Resource.create({"service.name": os.environ.get("OTEL_SERVICE_NAME", "table-order-backend")})
    exporter = OTLPMetricExporter(endpoint=endpoint, insecure=True)
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=10000)
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)

    global meter, orders_created, sse_connections, recommendations_generated
    global http_request_count, http_request_duration, http_active_requests
    meter = metrics.get_meter("table-order")
    orders_created = meter.create_counter("orders_created", unit="1", description="Total orders created")
    sse_connections = meter.create_up_down_counter("sse_active_connections", unit="1", description="Active SSE connections")
    recommendations_generated = meter.create_counter("recommendations_generated", unit="1", description="Total recommendations generated")
    http_request_count = meter.create_counter("http_server_requests", unit="1", description="Total HTTP requests")
    http_request_duration = meter.create_histogram("http_server_request_duration_seconds", unit="s", description="HTTP request duration")
    http_active_requests = meter.create_up_down_counter("http_server_active_requests", unit="1", description="Active HTTP requests")
