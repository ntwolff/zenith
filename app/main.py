# app/main.py
from app.faust.app import faust_app
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.neo4j_database import Neo4jDatabase
from app.api.router import router as api_router
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    #faust_app.discover()
    #await asyncio.ensure_future(faust_app.start(), loop=asyncio.get_event_loop())
    yield
    #await faust_app.stop()

# FastAPI
app = fastapi_app = FastAPI(
    lifespan=lifespan,
    title="Fraud Detection",
    description="Detect fraudulent activity in near real-time.",
    version="0.0.1",
)
fastapi_app.include_router(api_router, prefix="/api")