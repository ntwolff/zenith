from unittest.mock import MagicMock
import pytest
from app.events.processors import CustomerRegistrationEventProcessor, LoginEventProcessor

@pytest.fixture
def mock_graph_database():
    graph_db = MagicMock()
    return graph_db

def test_process_customer_registration_event(mock_graph_database):
    processor = CustomerRegistrationEventProcessor(mock_graph_database)
    fake_event = MagicMock()
    processor.process(fake_event)
    # Verify that the database methods were called correctly
    assert mock_graph_database.create_customer_node.called
    assert mock_graph_database.create_registration_relationship.called
    assert mock_graph_database.create_device_node.called
    assert mock_graph_database.create_ip_address_node.called
    assert mock_graph_database.create_customer_device_relationship.called
    assert mock_graph_database.create_customer_ip_address_relationship.called

def test_process_login_event(mock_graph_database):
    processor = LoginEventProcessor(mock_graph_database)
    fake_event = MagicMock()
    processor.process(fake_event)
    # Verify that the relevant database methods were called
    assert mock_graph_database.create_login_relationship.called
    assert mock_graph_database.create_device_node.called
    assert mock_graph_database.create_ip_address_node.called
    assert mock_graph_database.create_customer_device_relationship.called
    assert mock_graph_database.create_customer_ip_address_relationship.called
