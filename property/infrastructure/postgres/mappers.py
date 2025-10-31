from abc import ABC, abstractmethod

from property.domain.models import BaseEntity
from property.domain.models import Configuration
from property.domain.models import Property
from property.domain.models import Location
from property.infrastructure.postgres.tables import BaseTable
from property.infrastructure.postgres.tables import ConfigurationTable
from property.infrastructure.postgres.tables import PropertyTable


class BaseMapper(ABC):
    @abstractmethod
    def to_table(self, entity: BaseEntity) -> BaseTable:
        pass

    @abstractmethod
    def to_domain(self, entity: BaseTable) -> BaseEntity:
        pass


class PropertyMapper(BaseMapper):
    def to_table(self, entity: Property) -> PropertyTable:
        return PropertyTable(
            id=entity.id,
            room_count=entity.room_count,
            bathroom_count=entity.bathroom_count,
            location_address=entity.location.address,
            location_latitude=entity.location.latitude,
            location_longitude=entity.location.longitude,
            rent_value=entity.rent_value,
            property_type=entity.property_type,
            additional_features=entity.additional_features,
        )

    def to_domain(self, entity: PropertyTable) -> Property:
        return Property(
            id=entity.id,
            room_count=entity.room_count,
            bathroom_count=entity.bathroom_count,
            location=Location(
                address=entity.location_address,
                latitude=entity.location_latitude,
                longitude=entity.location_longitude,
            ),
            rent_value=entity.rent_value,
            property_type=entity.property_type,
            additional_features=entity.additional_features,
        )


class ConfigurationMapper(BaseMapper):
    def to_table(self, entity: Configuration) -> ConfigurationTable:
        return ConfigurationTable(
            id=entity.id,
            key=entity.key,
            type=entity.type,
            value=entity.value,
        )

    def to_domain(self, entity: ConfigurationTable) -> Configuration:
        return Configuration(
            id=entity.id,
            key=entity.key,
            type=entity.type,
            value=entity.value,
        )
