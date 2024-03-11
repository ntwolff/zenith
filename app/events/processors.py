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
        # Perform other necessary actions

class LoginEventProcessor(EventProcessor):
    def __init__(self, graph_database):
        self.graph_database = graph_database

    def process(self, event):
        self.graph_database.create_login_relationship(event)
        # Perform other necessary actions