from fastapi import FastAPI
from app.graph import driver, get_customer_data, detect_communities, calculate_centrality
from .models import CustomerRegisteredEvent, CustomerAnalytics

app = FastAPI()

## /customers/{id}

@app.get("/customers/{customer_id}", response_model=CustomerRegisteredEvent)
async def get_customer(customer_id: str):
    with driver.session() as session:
        result = session.read_transaction(get_customer_data, customer_id)
        # Fetch additional data from RocksDB if needed
        return result

## /customers/{id}/analytics

@app.get("/customers/{customer_id}/analytics", response_model=CustomerAnalytics)
async def get_customer_analytics(customer_id: str):
    with driver.session() as session:
        communities = session.read_transaction(detect_communities)
        centrality = session.read_transaction(calculate_centrality, customer_id)
        return {"communities": communities, "centrality": centrality}