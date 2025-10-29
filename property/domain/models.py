from uuid import UUID
from pydantic import BaseModel, ConfigDict


class BaseEntity(BaseModel):
    model_config = ConfigDict(
        json_encoders={
            UUID: str,
        }
    )


class Location(BaseEntity):
    address: str
    latitude: float = None
    longitude: float = None


class Property(BaseEntity):
    id: UUID
    property_type: str  # TODO: Why emum config via settings?
    room_count: int
    bathroom_count: int
    additional_features: list[str]  # TODO: Why emum config via settings?
    location: Location
    rent_value: float
