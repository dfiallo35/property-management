from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from property.domain.exceptions import ConfigurationNotValidError
from property.domain.exceptions import NotValidPropertyError
from property.domain.exceptions import NotAllAdditionalFeatureError
from property.domain.exceptions import NotValidValueAdditionalFeatureError
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
    additional_features: dict
    location: Location
    rent_value: float

    def is_valid_property_type(self, configurations: list["Configuration"]):
        if not configurations:
            raise NotValidPropertyError(self.property_type)

    def is_valid_additional_features(self, configurations: list["Configuration"]):
        if len(self.additional_features.keys()) != len(configurations):
            raise NotAllAdditionalFeatureError()
        for conf in configurations:
            val = self.additional_features.get(conf.key)
            if conf.type == ConfigurationType.SELECT:
                if val not in conf.value:
                    raise NotValidValueAdditionalFeatureError(
                        key=conf.key, invalid_value=val
                    )
            elif conf.type == ConfigurationType.NUMBER and not isinstance(val, int):
                raise NotValidValueAdditionalFeatureError(
                    key=conf.key, invalid_value=val
                )
            elif conf.type == ConfigurationType.TEXT and val is not None:
                raise NotValidValueAdditionalFeatureError(
                    key=conf.key, invalid_value=val
                )


class Configuration(BaseEntity):
    key: str
    type: ConfigurationType
    value: list[str] | None = None

    def is_valid_configuration(self):
        if self.type != ConfigurationType.SELECT and self.value is not None:
            raise ConfigurationNotValidError(key=self.key, type=self.type)
        return True
