from uuid import uuid4
import pytest_asyncio
from httpx import ASGITransport
from httpx import AsyncClient
from factory.alchemy import SQLAlchemyModelFactory

from property.infrastructure.postgres.tables import BaseTable
from property.infrastructure.postgres.database import DbConnection
from property.infrastructure.postgres.tables import ConfigurationTable
from property.infrastructure.postgres.tables import PropertyTable

from main import app
from main import container


@pytest_asyncio.fixture(scope="function")
async def db_connection():
    db = container.db_connection()
    yield db
    await db.engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="function", autouse=True)
async def reset_db(db_connection: DbConnection):
    async with db_connection.engine.begin() as conn:
        await conn.run_sync(BaseTable.metadata.drop_all)
        await conn.run_sync(BaseTable.metadata.create_all)


class AsyncBaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    @classmethod
    async def create_async(cls, **kwargs):
        if cls._meta.sqlalchemy_session is None:
            raise ValueError(
                "sqlalchemy_session must be set before calling create_async()"
            )

        obj = cls(**kwargs)
        await cls._meta.sqlalchemy_session.commit()
        await cls._meta.sqlalchemy_session.refresh(obj)
        return obj


class PropertyFactory(AsyncBaseFactory):
    class Meta:
        model = PropertyTable


class ConfigurationFactory(AsyncBaseFactory):
    class Meta:
        model = ConfigurationTable


@pytest_asyncio.fixture
async def create_property(db_connection):
    async with db_connection.get_session() as session:
        PropertyFactory._meta.sqlalchemy_session = session
        property = await PropertyFactory.create_async(
            id=uuid4(),
            property_type="test",
            room_count=1,
            bathroom_count=1,
            additional_features=["feature1", "feature2"],
            location_address="test",
            location_latitude=1.0,
            location_longitude=1.0,
            rent_value=1.0,
        )
        yield property


@pytest_asyncio.fixture
async def create_configuration(db_connection):
    async with db_connection.get_session() as session:
        ConfigurationFactory._meta.sqlalchemy_session = session
        configuration = await ConfigurationFactory.create_async(
            id=uuid4(),
            key="test",
            value=["test1", "test2"],
        )
        yield configuration
