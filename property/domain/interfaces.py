from abc import ABC
from abc import abstractmethod

from property.domain.models import BaseEntity


class IBaseRepository(ABC):
    @abstractmethod
    async def create(self) -> BaseEntity:
        pass

    @abstractmethod
    async def list(self, filters) -> list[BaseEntity]:
        pass

    @abstractmethod
    async def delete(self) -> None:
        pass

    @abstractmethod
    async def update(self) -> BaseEntity:
        pass


class IPropertyRepository(IBaseRepository):
    pass


class IConfigurationRepository(IBaseRepository):
    pass
