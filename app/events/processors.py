from abc import ABC, abstractmethod
from .models import CustomerRegistrationEvent, LoginEvent
from ..graph.database import GraphDatabase

class EventProcessor(ABC):
    @abstractmethod
    def process(self, event):
        pass

class CustomerRegistrationEventProcessor(EventProcessor):
    def __init__(self, graph_database):
        self.graph_database = graph_database

    def process(self, event):
        self.graph_database.create_customer_node(event)
        self.graph_database.create_device_node(event.device)
        self.graph_database.create_ip_address_node(event.ip_address)
        self.graph_database.create_customer_device_relationship(event.customer_id, event.device.device_id)
        self.graph_database.create_customer_ip_address_relationship(event.customer_id, event.ip_address.ip)
        # Perform other necessary actions

class LoginEventProcessor(EventProcessor):
    def __init__(self, graph_database):
        self.graph_database = graph_database

    def process(self, event):
        self.graph_database.create_login_relationship(event)
        self.graph_database.create_device_node(event.device)
        self.graph_database.create_ip_address_node(event.ip_address)
        self.graph_database.create_customer_device_relationship(event.customer_id, event.device.device_id)
        self.graph_database.create_customer_ip_address_relationship(event.customer_id, event.ip_address.ip)
        # Perform other necessary actions