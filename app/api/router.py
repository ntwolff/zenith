from fastapi import APIRouter
from app.api.endpoints import events, fraud

router = APIRouter()

# Register endpoint modules
router.include_router(events.router, prefix="/events", tags=["customers"])
router.include_router(fraud.router, prefix="/fraud", tags=["fraud"])