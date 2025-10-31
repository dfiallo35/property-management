from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from uuid import UUID

from property.application.dtos import ConfigurationOutput
from property.application.dtos import ConfigurationCreateRequest
from property.application.dtos import ConfigurationUpdateRequest
from property.application.exceptions import ExceptionResponse
from property.application.services import ConfigurationService
from property.application.services import get_configuration_service
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
async def create_configuration(
    create_request: ConfigurationCreateRequest,
    service: ConfigurationService = Depends(get_configuration_service),
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
async def list_configurations(
    filters: ConfigurationFilter = Depends(),
    service: ConfigurationService = Depends(get_configuration_service),
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
async def get_configuration(
    property_id: UUID,
    service: ConfigurationService = Depends(get_configuration_service),
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
async def update_configuration(
    property_id: UUID,
    update_request: ConfigurationUpdateRequest,
    service: ConfigurationService = Depends(get_configuration_service),
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
async def delete_configuration(
    property_id: UUID,
    service: ConfigurationService = Depends(get_configuration_service),
):
    return await service.delete_configuration(property_id)
