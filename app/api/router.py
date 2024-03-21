from fastapi import APIRouter
from app.api.endpoints import event
from app.api.endpoints import fraud
from app.api.endpoints import graph
from app.api.endpoints import foo


router = APIRouter()

# Register endpoint modules
router.include_router(event.router, prefix="/events", tags=["events"])
router.include_router(fraud.router, prefix="/fraud", tags=["fraud"])
router.include_router(graph.router, prefix="/graph", tags=["graph"])
router.include_router(foo.router, prefix="/foo", tags=["foo"])