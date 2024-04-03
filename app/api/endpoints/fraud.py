"""
FastAPI Fraud Endpoints
"""
from fastapi import APIRouter, Depends
from app.database.neo4j import Neo4jDatabase
from app.services import FraudService
from app.models import RiskSignal, Event
from app.utils.graph import GraphHelper
from app.config.settings import settings
from app.database.manager import DatabaseManager
from app.database.repositories.graph import GraphRepository

def get_db():
    db_manager = DatabaseManager(settings)
    graph_repo = GraphRepository(db_manager)
    db = graph_repo.db
    try:
        yield db
    finally:
        db.close()

fraud_service = FraudService(Depends(get_db))
router = APIRouter()

# ----------------------------------------------
# Endpoints
# ----------------------------------------------

@router.post("/fraud/process", status_code=204)
async def process_fraud(signal: RiskSignal):
    await fraud_service.process_fraud(signal=signal)


@router.post("/fraud/clear", status_code=204) 
async def clear_fraud_status(event: Event):
    await fraud_service.mark_as_cleared(event)


@router.get("/fraud/score")
async def fraud_scores(limit: int = 10, db: Neo4jDatabase = Depends(get_db)):
    """
    Composite Graph algorithms
    """
    get_fraud_scores(db, limit)


# ----------------------------------------------
# Helpers
# ----------------------------------------------

def get_fraud_scores(db, limit):
    graph_name = "fraud_graph"
    util = GraphHelper()

    util.drop_graph(db, graph_name)
    util.create_graph(db, graph_name)

    result = util.run_algorithm(db, "pageRank", graph_name, limit)
    records = result.data()

    risk_scores = [{
        "label": record["label"], "id": record["id"], "properties": record["properties"], 
        "score": record["score"]} for record in records]

    return {"page_rank_scores": risk_scores}