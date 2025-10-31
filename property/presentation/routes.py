from fastapi import APIRouter

from property.presentation.configuration_api import router as configuration_router
from property.presentation.property_api import router as property_router

router = APIRouter()

router.include_router(property_router)
router.include_router(configuration_router)
