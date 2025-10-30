from uuid import UUID
from pydantic import BaseModel, ConfigDict


class BaseEntity(BaseModel):
    id: UUID

    model_config = ConfigDict(
        json_encoders={
            UUID: str,
        }
    )


class Location(BaseEntity):
    address: str
    latitude: float | None = None
    longitude: float | None = None


class Property(BaseEntity):
    property_type: str
    room_count: int
    bathroom_count: int
    additional_features: list[str]
    location: Location
    rent_value: float


class Configuration(BaseEntity):
    key: str
    value: list[str]
