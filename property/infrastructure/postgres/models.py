from uuid import uuid4
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class Property(BaseModel):
    __tablename__ = "property"

    room_count: Mapped[int] = mapped_column(Integer, nullable=False)
    bathroom_count: Mapped[int] = mapped_column(Integer, nullable=False)
    location_address: Mapped[str] = mapped_column(String, nullable=False)
    location_latitude: Mapped[float] = mapped_column(Float, nullable=True)
    location_longitude: Mapped[float] = mapped_column(Float, nullable=True)
    rent_value: Mapped[Float] = mapped_column(Float, nullable=False)

    property_type: Mapped[str] = mapped_column(String, nullable=False)
    additional_features: Mapped[list[str]] = mapped_column(JSON, default=list)


class Configuration(BaseModel):
    __tablename__ = "configuration"

    key: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[list[str]] = mapped_column(JSON, nullable=False)
