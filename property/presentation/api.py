from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from uuid import UUID

from property.application.dtos import PropertyOutput
from property.application.dtos import PropertyCreateRequest
from property.application.dtos import PropertyUpdateRequest
from property.application.exceptions import ExceptionResponse
from property.application.services import PropertyService
from property.application.services import get_property_service
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
async def create_property(
    create_request: PropertyCreateRequest,
    service: PropertyService = Depends(get_property_service),
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
async def list_properties(
    filters: PropertyFilter = Depends(),
    service: PropertyService = Depends(get_property_service),
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
async def get_property(
    property_id: UUID,
    service: PropertyService = Depends(get_property_service),
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
async def update_property(
    property_id: UUID,
    update_request: PropertyUpdateRequest,
    service: PropertyService = Depends(get_property_service),
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
async def delete_property(
    property_id: UUID,
    service: PropertyService = Depends(get_property_service),
):
    return await service.delete_property(property_id)
