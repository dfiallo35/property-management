from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from pydantic_settings import BaseSettings

from property.domain.interfaces import IPropertyRepository
from property.infrastructure.postgres.database import DbConnection
from property.infrastructure.postgres.repositories import PropertyRepositoryPostgres


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        packages=["property"],
    )

    config = providers.Configuration()

    db_connection = providers.Singleton(DbConnection, config.DATABASE_URL)

    property_repository = providers.Singleton(
        PropertyRepositoryPostgres, db_connection=db_connection
    )

    repositories = providers.Dict(
        {
            IPropertyRepository: property_repository,
        }
    )


def create_container() -> Container:
    settings = Settings()
    container = Container()
    container.config.from_pydantic(settings)
    container.init_resources()
    container.wire(modules=[__name__, "property.application.services"])
    return container
