import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import fastapi_app

client = TestClient(fastapi_app)

@pytest.fixture
def mock_db_methods():
    with patch('app.api.endpoints.Neo4jGraphDatabase') as mock_db_class:
        mock_db_instance = mock_db_class.return_value
        mock_db_instance.create_customer_node.return_value = None
        mock_db_instance.create_customer_event_relationship.return_value = None
        mock_db_instance.create_device_node.return_value = None
        mock_db_instance.create_ip_address_node.return_value = None
        mock_db_instance.create_customer_device_relationship.return_value = None
        mock_db_instance.create_customer_ip_address_relationship.return_value = None
        yield mock_db_instance

def test_customer_registration_endpoint(mock_db_methods):
    payload = {
        #"event_id": "test-event",
        #"event_type": "registration",
        "customer_id": "test-customer",
        "timestamp": "2021-01-01T00:00:00Z",
        "email": "test@example.com",
        "phone_number": "123456789",
        "person": {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "ssn": "123-45-6789",
            "address": {
                "address_id": "test-address",
                "street_address": "123 Main St",
                "city": "Springfield",
                "state": "IL",
                "zip_code": "62701"
            }
        },
        "device": {
            "device_id": "test-device",
            "user_agent": "test-agent"
        },
        "ip_address": {
            "ip": "192.168.1.1"
        }
    }
    response = client.post("/api/events/customer-registration", json=payload)
    assert response.status_code == 200
    mock_db_methods.create_customer_node.assert_called_once()
    #mock_db_methods.create_customer_event_relationship.assert_called_once()

def test_login_event_endpoint(mock_db_methods):
    payload = {
        #"event_id": "test-event",
        #"event_type": "login",
        "customer_id": "test-customer",
        "timestamp": "2021-01-01T00:00:00Z",
        "device": {
            "device_id": "test-device",
            "user_agent": "test-agent"
        },
        "ip_address": {
            "ip": "192.168.1.1"
        }
    }
    response = client.post("/api/events/login", json=payload)
    assert response.status_code == 200
    mock_db_methods.create_customer_event_relationship.assert_called_once()