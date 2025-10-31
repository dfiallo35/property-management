from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from uuid import UUID

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from property.settings import Container
from property.application.dtos import ConfigurationOutput
from property.application.dtos import ConfigurationCreateRequest
from property.application.dtos import ConfigurationUpdateRequest
from property.application.exceptions import ExceptionResponse
from property.application.services import ConfigurationService
from property.domain.filters import ConfigurationFilter


router = APIRouter(prefix="/api/properties/settings", tags=["Configurations"])


@router.post(
    "/",
    responses={
        status.HTTP_201_CREATED: {"model": ConfigurationOutput},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
    },
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_configuration(
    create_request: ConfigurationCreateRequest,
    service: ConfigurationService = Depends(Provide[Container.configuration_service]),
):
    return await service.create_configuration(create_request)


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": list[ConfigurationOutput]},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def list_configurations(
    filters: ConfigurationFilter = Depends(),
    service: ConfigurationService = Depends(Provide[Container.configuration_service]),
):
    return await service.list_configurations(filters)


@router.get(
    "/{property_id}",
    responses={
        status.HTTP_200_OK: {"model": ConfigurationOutput},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_configuration(
    property_id: UUID,
    service: ConfigurationService = Depends(Provide[Container.configuration_service]),
):
    return await service.get_configuration_by_id(property_id)


@router.put(
    "/{property_id}",
    responses={
        status.HTTP_200_OK: {"model": ConfigurationOutput},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def update_configuration(
    property_id: UUID,
    update_request: ConfigurationUpdateRequest,
    service: ConfigurationService = Depends(Provide[Container.configuration_service]),
):
    return await service.update_configuration(property_id, update_request)


@router.delete(
    "/{property_id}",
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_configuration(
    property_id: UUID,
    service: ConfigurationService = Depends(Provide[Container.configuration_service]),
):
    return await service.delete_configuration(property_id)
