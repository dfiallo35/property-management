from uuid import UUID

from property.application.dtos import ConfigurationCreateRequest
from property.application.dtos import PropertyCreateRequest
from property.application.dtos import ConfigurationUpdateRequest
from property.application.dtos import PropertyUpdateRequest
from property.application.dtos import ConfigurationOutput
from property.application.dtos import PropertyOutput
from property.domain.exceptions import PropertyNotFoundError
from property.application.mappers import ConfigurationMapper
from property.application.mappers import PropertyMapper
from property.domain.filters import ConfigurationFilter
from property.domain.filters import PropertyFilter
from property.domain.interfaces import IConfigurationRepository
from property.domain.interfaces import IPropertyRepository


class PropertyService:
    def __init__(
        self,
        property_repository: IPropertyRepository,
        configuration_repository: IConfigurationRepository,
    ):
        self.property_repository = property_repository
        self.configuration_repository = configuration_repository
        self.mapper = PropertyMapper()

    async def create_property(
        self, create_request: PropertyCreateRequest
    ) -> PropertyOutput:
        entity = self.mapper.to_domain(create_request)

        property_type_config = await self.configuration_repository.list(
            ConfigurationFilter(key_eq=create_request.property_type)
        )
        entity.is_valid_property_type(property_type_config)
        additional_features_config = await self.configuration_repository.list(
            ConfigurationFilter(key_in=list(entity.additional_features.keys()))
        )
        entity.is_valid_additional_features(additional_features_config)

        created_entity = await self.property_repository.create(entity)
        return self.mapper.to_api(created_entity)

    async def list_properties(self, filters: PropertyFilter):
        entities = await self.property_repository.list(filters)
        return [self.mapper.to_api(entity) for entity in entities]

    async def get_property_by_id(self, id: UUID):
        filter = PropertyFilter(id_eq=id)
        entities = await self.property_repository.list(filter)
        if len(entities) == 0:
            raise PropertyNotFoundError(id)
        return self.mapper.to_api(entities[0])

    async def update_property(self, id: UUID, update_request: PropertyUpdateRequest):
        entity = await self.get_property_by_id(id)
        if not entity:
            raise PropertyNotFoundError(id)
        updated_entity = self.mapper.to_update(entity, update_request)

        if update_request.property_type:
            property_type_config = await self.configuration_repository.list(
                ConfigurationFilter(key_eq=update_request.property_type)
            )
            updated_entity.is_valid_property_type(property_type_config)
        if update_request.additional_features:
            additional_features_config = await self.configuration_repository.list(
                ConfigurationFilter(key_in=list(entity.additional_features.keys()))
            )
            entity.is_valid_additional_features(additional_features_config)

        entity = await self.property_repository.update(updated_entity)
        return self.mapper.to_api(entity)

    async def delete_property(self, id: UUID):
        entity = await self.get_property_by_id(id)
        if not entity:
            raise PropertyNotFoundError(id)
        return await self.property_repository.delete(entity)


class ConfigurationService:
    def __init__(
        self,
        configuration_repository: IConfigurationRepository,
    ):
        self.configuration_repository = configuration_repository
        self.mapper = ConfigurationMapper()

    async def create_configuration(
        self, create_request: ConfigurationCreateRequest
    ) -> ConfigurationOutput:
        entity = self.mapper.to_domain(create_request)
        entity.is_valid_configuration()
        created_entity = await self.configuration_repository.create(entity)
        return self.mapper.to_api(created_entity)

    async def list_configurations(self, filters: ConfigurationFilter):
        entities = await self.configuration_repository.list(filters)
        return [self.mapper.to_api(entity) for entity in entities]

    async def get_configuration_by_id(self, id: UUID):
        filter = ConfigurationFilter(id_eq=id)
        entities = await self.configuration_repository.list(filter)
        if len(entities) == 0:
            raise PropertyNotFoundError(id)
        return self.mapper.to_api(entities[0])

    async def update_configuration(
        self, id: UUID, update_request: ConfigurationUpdateRequest
    ):
        entity = await self.get_configuration_by_id(id)
        if not entity:
            raise PropertyNotFoundError(id)
        updated_entity = self.mapper.to_update(entity, update_request)
        updated_entity.is_valid_configuration()
        entity = await self.configuration_repository.update(updated_entity)
        return self.mapper.to_api(entity)

    async def delete_configuration(self, id: UUID):
        entity = await self.get_configuration_by_id(id)
        if not entity:
            raise PropertyNotFoundError(id)
        return await self.configuration_repository.delete(entity)
