import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TableMessage(Base):
    __tablename__ = "table_messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    store_id: Mapped[str] = mapped_column(String(36), ForeignKey("stores.id"), nullable=False)
    from_table_id: Mapped[str] = mapped_column(String(36), ForeignKey("tables.id"), nullable=False)
    to_table_id: Mapped[str] = mapped_column(String(36), ForeignKey("tables.id"), nullable=False)
    from_table_number: Mapped[int] = mapped_column(Integer, nullable=False)
    to_table_number: Mapped[int] = mapped_column(Integer, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
