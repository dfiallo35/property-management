from pydantic import BaseModel

from property.domain.enums import ConfigurationType


class BaseCreateRequest(BaseModel):
    pass


class BaseUpdateRequest(BaseModel):
    pass


class BaseOutput(BaseModel):
    pass


class LocationCreateRequest(BaseCreateRequest):
    address: str
    latitude: float | None = None
    longitude: float | None = None


class PropertyCreateRequest(BaseCreateRequest):
    property_type: str
    room_count: int
    bathroom_count: int
    additional_features: list[str]
    location: LocationCreateRequest
    rent_value: float


class PropertyUpdateRequest(BaseUpdateRequest):
    property_type: str | None = None
    room_count: int | None = None
    bathroom_count: int | None = None
    additional_features: list[str] | None = None
    location: LocationCreateRequest | None = None
    rent_value: float | None = None


class LocationOutput(BaseOutput):
    address: str
    latitude: float | None = None
    longitude: float | None = None


class PropertyOutput(BaseOutput):
    id: str
    property_type: str
    room_count: int
    bathroom_count: int
    additional_features: list[str]
    location: LocationOutput
    rent_value: float


class ConfigurationOutput(BaseOutput):
    id: str
    key: str
    type: ConfigurationType
    value: list[str] | None = None


class ConfigurationCreateRequest(BaseCreateRequest):
    key: str
    type: ConfigurationType
    value: list[str] | None = None


class ConfigurationUpdateRequest(BaseUpdateRequest):
    key: str | None = None
    type: ConfigurationType | None = None
    value: list[str] | None = None
