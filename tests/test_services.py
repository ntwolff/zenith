from unittest.mock import MagicMock, patch
import pytest
from app.services.device_service import DeviceService
from app.services.ip_address_service import IpAddressService
from app.services.address_service import AddressService
from app.services.customer_service import CustomerService
from app.services.event_service import EventService
from app.models import CustomerEvent, Customer, Device, IpAddress, Address
from textwrap import dedent

@pytest.fixture
def mock_graph_database():
    graph_db = MagicMock()
    return graph_db

def fake_customer_event():
    return CustomerEvent(
        id="123",
        type="registration",
        timestamp=1710252476000,
        customer=Customer(
            id="123",
            email="test@example.com",
            phone="1234567890",
            first_name="John",
            last_name="Doe",
            date_of_birth="1990-01-01",
            ssn="123-45-6789",
            address=Address(
                id="456",
                street="123 Main St",
                city="Springfield",
                state="IL",
                zip="62701"
            )
        ),
        device=Device(id="456",user_agent="Mozilla/5.0"),
        ip_address=IpAddress(id="000.00.0.00", ipv4="000.00.0.00")
    )

def test_device_service_upsert(mock_graph_database, fake_event=fake_customer_event()):
    device_service = DeviceService(mock_graph_database)
    device_service.upsert(fake_event.device)
    assert mock_graph_database.execute_query.called

def test_ip_address_service_upsert(mock_graph_database, fake_event=fake_customer_event()):
    ip_address_service = IpAddressService(mock_graph_database)
    ip_address_service.upsert(fake_event.ip_address)
    assert mock_graph_database.execute_query.called

def test_ip_address_service_mark_as_risky(mock_graph_database):
    ip_address_service = IpAddressService(mock_graph_database)
    ip_address_service.mark_as_risky("192.168.1.1", "High Velocity IP")
    assert mock_graph_database.execute_query.called

def test_address_service_upsert(mock_graph_database, fake_event=fake_customer_event()):
    address_service = AddressService(mock_graph_database)
    address_service.upsert(fake_event.customer.address)
    assert mock_graph_database.execute_query.called

def test_customer_service_upsert(mock_graph_database, fake_event=fake_customer_event()):
    customer_service = CustomerService(mock_graph_database)
    customer_service.upsert(fake_event.customer)
    assert mock_graph_database.execute_query.called

def test_customer_service_mark_as_risky(mock_graph_database):
    customer_service = CustomerService(mock_graph_database)
    customer_service.mark_as_risky("customer_id", "High Velocity Logins")
    assert mock_graph_database.execute_query.called

def test_event_service_create(mock_graph_database, fake_event=fake_customer_event()):
    event_service = EventService(mock_graph_database)
    event_service.create(fake_event)
    assert mock_graph_database.execute_query.called
