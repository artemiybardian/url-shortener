import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from analytics_service.database import Base


class Click(Base):
    __tablename__ = "clicks"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    url_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    short_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)
    user_agent: Mapped[str] = mapped_column(String(1024), default="")
    referrer: Mapped[str] = mapped_column(String(2048), default="")
    country: Mapped[str] = mapped_column(String(2), default="")
    clicked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
