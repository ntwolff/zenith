"""
FastAPI Application
"""

# from app.stream.faust_app import faust_app
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.router import router as api_router

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI): # pylint: disable=unused-argument
    """
    FastAPI context manager
    """
    #@TODO: Pre Start-up Tasks
    yield
    #@TODO: Pre Shut-down Tasks

app = FastAPI(
    lifespan=lifespan,
    title="Zenith API",
    description="Detect fraudulent activity in near real-time.",
    version="0.0.1",
)
app.include_router(api_router, prefix="/api")

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"}
    )
