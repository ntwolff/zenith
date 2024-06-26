"""
FastAPI Routers
"""

from fastapi import APIRouter
from app.api.endpoints import admin, fraud

router = APIRouter()

# Register Sub-routers
router.include_router(admin.router, tags=["Admin"])
router.include_router(fraud.router, tags=["Fraud"])
