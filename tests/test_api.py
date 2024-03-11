from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import fastapi_app  # Adjust import as necessary

client = TestClient(fastapi_app)

@patch('app.api.endpoints.Neo4jGraphDatabase')
def test_customer_registration_endpoint(mock_db_class):
    # Mock the methods used by CustomerRegistrationEventProcessor
    mock_db_instance = mock_db_class.return_value
    mock_db_instance.create_customer_node.return_value = None
    mock_db_instance.create_device_node.return_value = None
    mock_db_instance.create_ip_address_node.return_value = None
    mock_db_instance.create_customer_device_relationship.return_value = None
    mock_db_instance.create_customer_ip_address_relationship.return_value = None

    payload = {
        "customer_id": "test-customer",
        "email": "test@example.com",
        "phone_number": "123456789",
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
    mock_db_instance.create_customer_node.assert_called_once()

@patch('app.api.endpoints.Neo4jGraphDatabase')
def test_login_event_endpoint(mock_db_class):
    # Mock the methods used by LoginEventProcessor
    mock_db_instance = mock_db_class.return_value
    mock_db_instance.create_login_relationship.return_value = None
    mock_db_instance.create_device_node.return_value = None
    mock_db_instance.create_ip_address_node.return_value = None
    mock_db_instance.create_customer_device_relationship.return_value = None
    mock_db_instance.create_customer_ip_address_relationship.return_value = None

    payload = {
        "customer_id": "test-customer",
        "timestamp": 123456789.0,
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
    mock_db_instance.create_login_relationship.assert_called_once()