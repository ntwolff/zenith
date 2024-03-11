from abc import ABC, abstractmethod
from neo4j import GraphDatabase

class Neo4jGraphDatabase:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def create_customer_node(self, event):
        with self.driver.session() as session:
            session.run(
                "CREATE (c:Customer {customer_id: $customer_id, email: $email, phone_number: $phone_number})",
                customer_id=event.customer_id,
                email=event.email,
                phone_number=event.phone_number
            )

    def create_login_relationship(self, event):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (c:Customer {customer_id: $customer_id})
                CREATE (c)-[:LOGIN {timestamp: $timestamp}]->(:Login)
                """,
                customer_id=event.customer_id,
                timestamp=event.timestamp
            )