from sqlalchemy import select
from sqlalchemy.sql import Select

from property.domain.interfaces import IBaseRepository
from property.domain.interfaces import IConfigurationRepository
from property.domain.interfaces import IPropertyRepository
from property.domain.filters import BaseFilter
from property.domain.filters import ConfigurationFilter
from property.domain.filters import PropertyFilter
from property.domain.models import BaseEntity
from property.infrastructure.postgres.database import DbConnection
from property.infrastructure.postgres.tables import ConfigurationTable
from property.infrastructure.postgres.tables import PropertyTable
from property.infrastructure.postgres.mappers import ConfigurationMapper
from property.infrastructure.postgres.mappers import PropertyMapper


class BaseRepositoryPostgres(IBaseRepository):
    def __init__(self, db_connection: DbConnection):
        super().__init__()
        self.db_connection = db_connection

    async def filter(self, filters: PropertyFilter, query: Select) -> Select:
        if filters.limit:
            query = query.limit(filters.limit)
        if filters.offset:
            query = query.offset(filters.offset)
        if filters.order_by:
            order_by = filters.order_by
            desc = order_by.startswith("-")
            order_by = order_by.lstrip("-")

            column = getattr(self.table_class, order_by, None)
            if column:
                query = query.order_by(column.desc() if desc else column)

        return query

    async def create(self, entity: BaseEntity):
        try:
            async with self.db_connection.get_session() as session:
                table_entity = self.mapper.to_table(entity)
                session.add(table_entity)
                await session.commit()
                await session.refresh(table_entity)
                return self.mapper.to_domain(table_entity)
        except Exception as e:
            raise e

    async def list(self, filters: BaseFilter) -> list[BaseEntity]:
        try:
            async with self.db_connection.get_session() as session:
                query = select(self.table_class)
                query = await self.filter(filters, query)
                results = await session.execute(query)
                return [self.mapper.to_domain(r) for r in results.scalars().all()]
        except Exception as e:
            raise e

    async def delete(self, entity: BaseEntity) -> None:
        try:
            async with self.db_connection.get_session() as session:
                table_entity = await session.get(self.table_class, entity.id)
                if not table_entity:
                    raise ValueError(f"Record with id {entity.id} not found")
                await session.delete(table_entity)
                await session.commit()
        except Exception as e:
            raise e

    async def update(self, entity: BaseEntity) -> BaseEntity:
        try:
            async with self.db_connection.get_session() as session:
                model = await session.get(self.table_class, entity.id)
                if not model:
                    raise ValueError(f"Record with id {entity.id} not found")

                for key, value in entity.model_dump(exclude_unset=True).items():
                    setattr(model, key, value)
                await session.commit()
                await session.refresh(model)
                return self.mapper.to_domain(model)
        except Exception as e:
            raise e


class PropertyRepositoryPostgres(IPropertyRepository, BaseRepositoryPostgres):
    mapper = PropertyMapper()
    table_class = PropertyTable

    async def filter(self, filters: PropertyFilter, query: Select) -> Select:
        query = await super().filter(filters, query)
        if filters.id_eq is not None:
            query = query.where(self.table_class.id == filters.id_eq)
        return query


class ConfigurationRepositoryPostgres(IConfigurationRepository, BaseRepositoryPostgres):
    mapper = ConfigurationMapper()
    table_class = ConfigurationTable

    async def filter(self, filters: ConfigurationFilter, query: Select) -> Select:
        query = await super().filter(filters, query)
        if filters.id_eq is not None:
            query = query.where(self.table_class.id == filters.id_eq)
        return query
