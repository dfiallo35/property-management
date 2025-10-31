from fastapi import APIRouter

from property.presentation.api import router as property_router

router = APIRouter()

router.include_router(property_router)
