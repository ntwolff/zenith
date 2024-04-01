from fastapi import APIRouter
from app.api.endpoints.v2 import admin, fraud

router = APIRouter()

# Register endpoint modules
router.include_router(admin.router, tags=["Admin"])
router.include_router(fraud.router, tags=["Fraud"])