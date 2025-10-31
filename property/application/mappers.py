from property.domain.models import Configuration
from property.domain.models import Property
from property.domain.models import Location
from property.application.dtos import ConfigurationOutput
from property.application.dtos import ConfigurationCreateRequest
from property.application.dtos import PropertyCreateRequest
from property.application.dtos import PropertyOutput
from property.application.dtos import LocationOutput


class PropertyMapper:
    def to_api(self, entity: Property) -> PropertyOutput:
        return PropertyOutput(
            id=str(entity.id),
            property_type=entity.property_type,
            room_count=entity.room_count,
            bathroom_count=entity.bathroom_count,
            additional_features=entity.additional_features,
            location=LocationOutput(
                address=entity.location.address,
                latitude=entity.location.latitude,
                longitude=entity.location.longitude,
            ),
            rent_value=entity.rent_value,
        )

    def to_domain(self, create_request: PropertyCreateRequest) -> Property:
        return Property(
            property_type=create_request.property_type,
            room_count=create_request.room_count,
            bathroom_count=create_request.bathroom_count,
            additional_features=create_request.additional_features,
            location=Location(
                address=create_request.location.address,
                latitude=create_request.location.latitude,
                longitude=create_request.location.longitude,
            ),
            rent_value=create_request.rent_value,
        )


class ConfigurationMapper:
    def to_api(self, entity: Configuration) -> ConfigurationOutput:
        return ConfigurationOutput(
            id=str(entity.id),
            key=entity.key,
            value=entity.value,
        )

    def to_domain(self, create_request: ConfigurationCreateRequest) -> Configuration:
        return Configuration(
            key=create_request.key,
            value=create_request.value,
        )
