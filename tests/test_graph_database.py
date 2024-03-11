from unittest.mock import MagicMock, patch
import pytest
from app.graph.database import Neo4jGraphDatabase
from app.events.models import RegistrationEvent, LoginEvent, Device, IpAddress, Person, Address
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
    return RegistrationEvent(
        event_id="123",
        event_type="registration",
        customer_id="123",
        timestamp="2020-01-01T00:00:00",
        email="test@example.com",
        phone_number="1234567890",
        person=Person(
            first_name="John",
            last_name="Doe",
            date_of_birth="1990-01-01",
            ssn="123-45-6789",
            address=Address(
                address_id="456",
                street_address="123 Main St",
                city="Springfield",
                state="IL",
                zip_code="62701"
            )
        ),
        device=Device(device_id="456", user_agent="Mozilla/5.0"),
        ip_address=IpAddress(ip="000.00.0.00")
    )

def fake_login_event():
    return LoginEvent(
        event_id="123",
        event_type="login",
        customer_id="123",
        timestamp="2020-01-01T00:00:00",
        device=Device(device_id="456", user_agent="Mozilla/5.0"),
        ip_address=IpAddress(ip="000.00.0.00")        
    )

def test_create_customer_node(mock_neo4j_database, fake_event=fake_customer_registration_event()):
    db, mock_session = mock_neo4j_database
    db.create_customer_node(fake_event)

    expected_query = dedent("""\
        MERGE (c:Customer {customer_id: $customer_id})
        ON CREATE SET c.email = $email, c.phone_number = $phone_number, c.first_name = $first_name, c.last_name = $last_name, c.date_of_birth = $date_of_birth, c.ssn = $ssn
        RETURN c
    """)

    mock_session.run.assert_called_once_with(
        expected_query,
        customer_id="123",
        email="test@example.com",
        phone_number="1234567890",
        first_name="John",
        last_name="Doe",
        date_of_birth="1990-01-01",
        ssn="123-45-6789"
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

def test_create_address_node(mock_neo4j_database, fake_event=fake_customer_registration_event()):
    db, mock_session = mock_neo4j_database
    db.create_address_node(fake_event.person.address)
    mock_session.run.assert_called_once_with(
        "MERGE (a:Address {address_id: $address_id}) SET a.street_address = $street_address, a.city = $city, a.state = $state, a.zip_code = $zip_code",
        address_id="456",
        street_address="123 Main St",
        city="Springfield",
        state="IL",
        zip_code="62701"
    )

def test_create_customer_device_relationship(mock_neo4j_database, fake_event=fake_customer_registration_event()):
    db, mock_session = mock_neo4j_database
    db.create_customer_device_relationship(fake_event.customer_id, fake_event.device.device_id, fake_event.timestamp)

    expected_query = dedent("""\
        MATCH (c:Customer {customer_id: $customer_id})
        MATCH (d:Device {device_id: $device_id})
        MERGE (c)-[r:USES_DEVICE]->(d)
        ON CREATE SET r.since = $timestamp
    """)

    mock_session.run.assert_called_once_with(
        expected_query,
        customer_id="123",
        device_id="456",
        timestamp="2020-01-01T00:00:00"
    )

def test_create_customer_ip_address_relationship(mock_neo4j_database):
    db, mock_session = mock_neo4j_database
    db.create_customer_ip_address_relationship("123", "000.00.0.00", "2020-01-01T00:00:00")

    expected_query = dedent("""\
        MATCH (c:Customer {customer_id: $customer_id})
        MATCH (i:IpAddress {ip: $ip})
        MERGE (c)-[r:HAS_IP_ADDRESS]->(i)
        ON CREATE SET r.since = $timestamp
    """)

    mock_session.run.assert_called_once_with(
        expected_query,
        customer_id="123",
        ip="000.00.0.00",
        timestamp="2020-01-01T00:00:00"
    )

def test_create_customer_address_relationship(mock_neo4j_database):
    db, mock_session = mock_neo4j_database
    db.create_customer_address_relationship("123", "456", "2020-01-01T00:00:00")

    expected_query = dedent("""\
        MATCH (c:Customer {customer_id: $customer_id})
        MATCH (a:Address {address_id: $address_id})
        MERGE (c)-[r:RESIDES_AT]->(d)
        ON CREATE SET r.since = $timestamp
    """)

    mock_session.run.assert_called_once_with(
        expected_query,
        customer_id="123",
        address_id="456",
        timestamp="2020-01-01T00:00:00"
    )

def test_create_login_relationship(mock_neo4j_database, fake_event=fake_login_event()):
    db, mock_session = mock_neo4j_database
    db.create_customer_event_relationship(fake_event)

    expected_query = dedent("""\
    MATCH (c:Customer {customer_id: $customer_id})
    CREATE (c)-[:PERFORMS {timestamp: $timestamp}]->(:Event {type: $event_type})
    """)

    mock_session.run.assert_called_once_with(
        expected_query,
        customer_id="123",
        timestamp="2020-01-01T00:00:00",
        event_type="login"
    )
    
def test_create_registration_relationship(mock_neo4j_database, fake_event=fake_customer_registration_event()):
    db, mock_session = mock_neo4j_database
    db.create_customer_event_relationship(fake_event)

    expected_query = dedent("""\
    MATCH (c:Customer {customer_id: $customer_id})
    CREATE (c)-[:PERFORMS {timestamp: $timestamp}]->(:Event {type: $event_type})
    """)

    mock_session.run.assert_called_once_with(
        expected_query,
        customer_id="123",
        timestamp="2020-01-01T00:00:00",
        event_type="registration"
    )
