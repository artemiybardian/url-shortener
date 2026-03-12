import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from shortener_service.database import Base


class URL(Base):
    __tablename__ = "urls"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    short_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    original_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
