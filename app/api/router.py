from fastapi import APIRouter
from app.api.endpoints import event
from app.api.endpoints import fraud
from app.api.endpoints import graph


router = APIRouter()

# Register endpoint modules
router.include_router(event.router, prefix="/events", tags=["events"])
router.include_router(fraud.router, prefix="/fraud", tags=["fraud"])