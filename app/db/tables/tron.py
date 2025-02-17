import uuid

from sqlalchemy import Column, DateTime, Float, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class TronInfo(Base):
    """Информация о кошельках TRON"""

    __tablename__ = "tron_info"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True, index=True)
    address = Column(String(length=42), unique=True, index=True, nullable=False)
    balance = Column(Float(), nullable=False)
    energy = Column(Integer(), nullable=False)
    bandwidth = Column(Integer(), nullable=False)

    created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
