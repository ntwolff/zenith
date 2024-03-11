from abc import ABC, abstractmethod
from textwrap import dedent
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

    def create_device_node(self, device):
        with self.driver.session() as session:
            session.run(
                "MERGE (d:Device {device_id: $device_id}) "
                "SET d.user_agent = $user_agent",
                device_id=device.device_id,
                user_agent=device.user_agent
            )

    def create_ip_address_node(self, ip_address):
        with self.driver.session() as session:
            session.run(
                "MERGE (i:IpAddress {ip: $ip})",
                ip=ip_address.ip
            )

    def create_registration_relationship(self, event):
        query = dedent("""\
            MATCH (c:Customer {customer_id: $customer_id})
            CREATE (c)-[:REGISTRATION {timestamp: $timestamp}]->(:Registration)
        """)

        with self.driver.session() as session:
            session.run(
                query,
                customer_id=event.customer_id,
                timestamp=event.timestamp
            )

    def create_login_relationship(self, event):
        query = dedent("""\
            MATCH (c:Customer {customer_id: $customer_id})
            CREATE (c)-[:LOGIN {timestamp: $timestamp}]->(:Login)
        """)

        with self.driver.session() as session:
            session.run(
                query,
                customer_id=event.customer_id,
                timestamp=event.timestamp
            )

    def create_customer_device_relationship(self, customer_id, device_id):
        query = dedent("""\
            MATCH (c:Customer {customer_id: $customer_id})
            MATCH (d:Device {device_id: $device_id})
            MERGE (c)-[:USES_DEVICE]->(d)
        """)
        
        with self.driver.session() as session:
            session.run(
                query,
                customer_id=customer_id,
                device_id=device_id
            )

    def create_customer_ip_address_relationship(self, customer_id, ip):
        query = dedent("""\
            MATCH (c:Customer {customer_id: $customer_id})
            MATCH (i:IpAddress {ip: $ip})
            MERGE (c)-[:HAS_IP_ADDRESS]->(i)
        """)

        with self.driver.session() as session:
            session.run(
                query,
                customer_id=customer_id,
                ip=ip
            )