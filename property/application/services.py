from uuid import UUID

from property.application.dtos import ConfigurationCreateRequest
from property.application.dtos import PropertyCreateRequest
from property.application.dtos import ConfigurationUpdateRequest
from property.application.dtos import PropertyUpdateRequest
from property.application.dtos import ConfigurationOutput
from property.application.dtos import PropertyOutput
from property.application.exceptions import PropertyNotFoundError
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
    ):
        self.property_repository = property_repository
        self.mapper = PropertyMapper()

    async def create_property(
        self, create_request: PropertyCreateRequest
    ) -> PropertyOutput:
        entity = self.mapper.to_domain(create_request)
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
        entity = await self.property_repository.update(
            entity, update_request.model_dump(exclude_unset=True)
        )
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
        entity = await self.configuration_repository.update(
            entity, update_request.model_dump(exclude_unset=True)
        )
        return self.mapper.to_api(entity)

    async def delete_configuration(self, id: UUID):
        entity = await self.get_configuration_by_id(id)
        if not entity:
            raise PropertyNotFoundError(id)
        return await self.configuration_repository.delete(entity)


def get_property_service():
    return PropertyService()


def get_configuration_service():
    return ConfigurationService()
