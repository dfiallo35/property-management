from uuid import UUID
from pydantic import BaseModel


class BaseFilter(BaseModel):
    size: int | None = None
    page: int | None = None
    order_by: str | None = None

    @property
    def offset(self) -> int | None:
        if self.page is None or self.size is None:
            return None
        return (self.page) * self.size

    @property
    def limit(self) -> int | None:
        return self.size if self.size is not None else None


class PropertyFilter(BaseFilter):
    id_eq: UUID | None = None


class ConfigurationFilter(BaseFilter):
    id_eq: UUID | None = None
    key_eq: str | None = None
    key_in: list[str] | None = None
