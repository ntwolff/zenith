from fastapi import APIRouter
from app.api.endpoints.v2 import domain

router = APIRouter()

# Register endpoint modules
router.include_router(domain.router, prefix="/v2", tags=["v2"])