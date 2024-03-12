from unittest.mock import MagicMock
import pytest
from app.processors import CustomerEventGraphProcessor

@pytest.fixture
def mock_graph_database():
    graph_db = MagicMock()
    return graph_db

def test_process_customer_event(mock_graph_database):
    processor = CustomerEventGraphProcessor(mock_graph_database)
    fake_event = MagicMock()
    processor.process(fake_event)
    # Verify that the database methods were called correctly
    assert mock_graph_database.execute_query.called
