from abc import ABC, abstractmethod
from .models import RegistrationEvent, LoginEvent
from ..graph.database import GraphDatabase
from ..velocity import check_ip_address_velocity

class EventProcessor(ABC):
    @abstractmethod
    def process(self, event):
        pass

class RegistrationEventProcessor(EventProcessor):
    def __init__(self, graph_database):
        self.graph_database = graph_database

    def process(self, event):
        self.graph_database.create_customer_node(event)
        self.graph_database.create_customer_event_relationship(event)
        self.graph_database.create_device_node(event.device)
        self.graph_database.create_ip_address_node(event.ip_address)
        self.graph_database.create_address_node(event.person.address)
        self.graph_database.create_customer_device_relationship(event.customer_id, event.device.device_id, event.timestamp)
        self.graph_database.create_customer_ip_address_relationship(event.customer_id, event.ip_address.ip, event.timestamp)
        self.graph_database.create_customer_address_relationship(event.customer_id, event.person.address.address_id, event.timestamp)

        if check_ip_address_velocity(event.ip_address.ip, event.timestamp):
            print(f"High velocity detected for IP address: {event.ip_address.ip}")

class LoginEventProcessor(EventProcessor):
    def __init__(self, graph_database):
        self.graph_database = graph_database

    def process(self, event):
        self.graph_database.create_customer_event_relationship(event)
        self.graph_database.create_device_node(event.device)
        self.graph_database.create_ip_address_node(event.ip_address)
        self.graph_database.create_customer_device_relationship(event.customer_id, event.device.device_id, event.timestamp)
        self.graph_database.create_customer_ip_address_relationship(event.customer_id, event.ip_address.ip, event.timestamp)

        if check_ip_address_velocity(event.ip_address.ip, event.timestamp):
            print(f"High velocity detected for IP address: {event.ip_address.ip}")