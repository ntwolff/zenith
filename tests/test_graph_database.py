from unittest.mock import MagicMock, patch
import pytest
from app.graph.database import Neo4jGraphDatabase
from app.events.models import CustomerRegistrationEvent, LoginEvent, Device, IpAddress
from textwrap import dedent

@pytest.fixture
def mock_neo4j_database():
    with patch('neo4j.GraphDatabase.driver') as mock_driver:
        mock_session = MagicMock()
        # Setup context manager to return mock_session on enter
        mock_driver.return_value.session.return_value.__enter__.return_value = mock_session
        db = Neo4jGraphDatabase(uri="bolt://localhost:7687", auth=("neo4j", "password"))
        yield db, mock_session

def fake_customer_registration_event():
    return CustomerRegistrationEvent(
        customer_id="123",
        email="test@example.com",
        phone_number="1234567890",
        device=Device(device_id="456", user_agent="Mozilla/5.0"),
        ip_address=IpAddress(ip="000.00.0.00")
    )

def test_create_customer_node(mock_neo4j_database, fake_event=fake_customer_registration_event()):
    db, mock_session = mock_neo4j_database
    db.create_customer_node(fake_event)
    mock_session.run.assert_called_once_with(
        "CREATE (c:Customer {customer_id: $customer_id, email: $email, phone_number: $phone_number})",
        customer_id="123",
        email="test@example.com",
        phone_number="1234567890"
    )

def test_create_device_node(mock_neo4j_database, fake_event=fake_customer_registration_event()):
    db, mock_session = mock_neo4j_database
    db.create_device_node(fake_event.device)
    mock_session.run.assert_called_once_with(
        "MERGE (d:Device {device_id: $device_id}) SET d.user_agent = $user_agent",
        device_id="456",
        user_agent="Mozilla/5.0"
    )

def test_create_ip_address_node(mock_neo4j_database, fake_event=fake_customer_registration_event()):
    db, mock_session = mock_neo4j_database
    db.create_ip_address_node(fake_event.ip_address)
    mock_session.run.assert_called_once_with(
        "MERGE (i:IpAddress {ip: $ip})",
        ip="000.00.0.00"
    )

def test_create_customer_device_relationship(mock_neo4j_database, fake_event=fake_customer_registration_event()):
    db, mock_session = mock_neo4j_database
    db.create_customer_device_relationship(fake_event.customer_id, fake_event.device.device_id)

    expected_query = dedent("""\
        MATCH (c:Customer {customer_id: $customer_id})
        MATCH (d:Device {device_id: $device_id})
        MERGE (c)-[:USES_DEVICE]->(d)
    """)

    mock_session.run.assert_called_once_with(
        expected_query,
        customer_id="123",
        device_id="456"
    )

def test_create_customer_ip_address_relationship(mock_neo4j_database):
    db, mock_session = mock_neo4j_database
    db.create_customer_ip_address_relationship("123", "000.00.0.00")

    expected_query = dedent("""\
        MATCH (c:Customer {customer_id: $customer_id})
        MATCH (i:IpAddress {ip: $ip})
        MERGE (c)-[:HAS_IP_ADDRESS]->(i)
    """)

    mock_session.run.assert_called_once_with(
        expected_query,
        customer_id="123",
        ip="000.00.0.00"
    )

# def test_create_login_relationship(mock_neo4j_database, fake_event=fake_login_event()):
#     db, mock_session = mock_neo4j_database
#     db.create_login_relationship(fake_event.customer_id, fake_event.timestamp)

#     expected_query = dedent("""\
#         MATCH (c:Customer {customer_id: $customer_id})
#         CREATE (c)-[:LOGIN {timestamp: $timestamp}]->(:Login)
#     """)

#     mock_session.run.assert_called_once_with(
#         expected_query,
#         customer_id="123",
#         timestamp="2020-01-01T00:00:00"
#     )
