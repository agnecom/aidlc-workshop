from __future__ import annotations
from datetime import datetime, timedelta, timezone

import structlog
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.dependencies.auth import create_access_token
from app.models.admin import Admin
from app.models.store import Store
from app.models.table import Table, TableSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = structlog.get_logger()


class AuthService:
    @staticmethod
    def admin_login(db: Session, store_identifier: str, username: str, password: str) -> dict:
        store = db.query(Store).filter(Store.store_identifier == store_identifier).first()
        if not store:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        admin = db.query(Admin).filter(Admin.store_id == store.id, Admin.username == username).first()
        if not admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if admin.locked_until and admin.locked_until > datetime.now(timezone.utc):
            logger.warning("account_locked", username=username)
            raise HTTPException(status_code=423, detail="Account locked. Try again later.")

        if not pwd_context.verify(password, admin.password_hash):
            admin.failed_login_attempts += 1
            if admin.failed_login_attempts >= settings.max_login_attempts:
                admin.locked_until = datetime.now(timezone.utc) + timedelta(minutes=settings.lockout_minutes)
                logger.warning("account_locked_due_to_attempts", username=username)
            db.commit()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        admin.failed_login_attempts = 0
        admin.locked_until = None
        db.commit()

        token = create_access_token({"sub": admin.id, "store_id": store.id, "role": "admin"})
        return {"access_token": token, "token_type": "bearer"}

    @staticmethod
    def table_login(db: Session, store_id: str, table_number: int, password: str) -> dict:
        store = db.query(Store).filter(
            (Store.id == store_id) | (Store.store_identifier == store_id)
        ).first()
        if not store:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        table = db.query(Table).filter(Table.store_id == store.id, Table.table_number == table_number).first()
        if not table or not pwd_context.verify(password, table.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        session = db.query(TableSession).filter(
            TableSession.table_id == table.id, TableSession.is_active == True
        ).first()

        if not session:
            session = TableSession(table_id=table.id)
            db.add(session)
            db.commit()
            db.refresh(session)

        token = create_access_token({
            "sub": table.id, "table_id": table.id, "table_number": table.table_number,
            "store_id": store.id, "session_id": session.id, "role": "table",
        })
        return {"access_token": token, "token_type": "bearer", "session_id": session.id}

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
