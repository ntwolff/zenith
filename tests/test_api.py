import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import fastapi_app

client = TestClient(fastapi_app)

def test_events_customer_event_endpoint(mock_event_db_methods):
    payload = {
        "id": "test-event",
        "type": "registration",
        "timestamp": "1710252476000",
        "customer": {
            "id": "test-customer",
            "email": "test@example.com",
            "phone": "123456789",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "ssn": "123-45-6789",
            "address": {
                "id": "test-address",
                "street": "123 Main St",
                "city": "Springfield",
                "state": "IL",
                "zip": "62701"
            }
        },
        "device": {
            "id": "test-device",
            "user_agent": "test-agent"
        },
        "ip_address": {
            "id": "192.168.1.1",
            "ipv4": "192.168.1.1"
        }
    }
    response = client.post("/api/events/customer-event", json=payload)
    assert response.status_code == 200

def test_fraud_centrality_endpoint(mock_fraud_db_methods):
    response = client.get("/api/fraud/centrality")
    assert response.status_code == 200

def test_fraud_page_rank(mock_fraud_db_methods):
    response = client.get("/api/fraud/page-rank")
    assert response.status_code == 200

def test_fraud_communities(mock_fraud_db_methods):
    response = client.get("/api/fraud/communities")
    assert response.status_code == 200

@pytest.fixture
def mock_event_db_methods():
    with patch('app.api.endpoints.events.graph_database') as mock_db_class:
        mock_db_instance = mock_db_class.return_value
        mock_db_instance.execute_query.return_value = None
        yield mock_db_instance()

@pytest.fixture
def mock_fraud_db_methods():
    with patch('app.api.endpoints.fraud.graph_database') as mock_db_class:
        mock_db_instance = mock_db_class.return_value
        mock_db_instance.execute_query.return_value = None
        yield mock_db_instance()