from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from property.domain.exceptions import ConfigurationNotValidError
from property.domain.enums import ConfigurationType


class BaseEntity(BaseModel):
    id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(
        json_encoders={
            UUID: str,
        }
    )


class Location(BaseModel):
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
    type: ConfigurationType
    value: list[str] | None = None

    def is_valid_configuration(self):
        if self.type != ConfigurationType.SELECT and self.value is not None:
            raise ConfigurationNotValidError(key=self.key, type=self.type)
        return True
