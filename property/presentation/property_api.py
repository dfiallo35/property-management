from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from uuid import UUID

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from property.settings import Container
from property.application.dtos import PropertyOutput
from property.application.dtos import PropertyCreateRequest
from property.application.dtos import PropertyUpdateRequest
from property.application.exceptions import ExceptionResponse
from property.application.services import PropertyService
from property.domain.filters import PropertyFilter


router = APIRouter(prefix="/api/properties", tags=["Properties"])


@router.post(
    "/",
    responses={
        status.HTTP_201_CREATED: {"model": PropertyOutput},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
    },
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_property(
    create_request: PropertyCreateRequest,
    service: PropertyService = Depends(Provide[Container.property_service]),
):
    return await service.create_property(create_request)


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": list[PropertyOutput]},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def list_properties(
    filters: PropertyFilter = Depends(),
    service: PropertyService = Depends(Provide[Container.property_service]),
):
    return await service.list_properties(filters)


@router.get(
    "/{property_id}",
    responses={
        status.HTTP_200_OK: {"model": PropertyOutput},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def get_property(
    property_id: UUID,
    service: PropertyService = Depends(Provide[Container.property_service]),
):
    return await service.get_property_by_id(property_id)


@router.put(
    "/{property_id}",
    responses={
        status.HTTP_200_OK: {"model": PropertyOutput},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def update_property(
    property_id: UUID,
    update_request: PropertyUpdateRequest,
    service: PropertyService = Depends(Provide[Container.property_service]),
):
    return await service.update_property(property_id, update_request)


@router.delete(
    "/{property_id}",
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_property(
    property_id: UUID,
    service: PropertyService = Depends(Provide[Container.property_service]),
):
    return await service.delete_property(property_id)
