from abc import ABC, abstractmethod
from textwrap import dedent
from neo4j import GraphDatabase

class Neo4jGraphDatabase:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)
        
    def create_customer_node(self, event):
        with self.driver.session() as session:
            query = dedent("""\
                MERGE (c:Customer {customer_id: $customer_id})
                ON CREATE SET c.email = $email, c.phone_number = $phone_number, c.first_name = $first_name, c.last_name = $last_name, c.date_of_birth = $date_of_birth, c.ssn = $ssn
                RETURN c
            """)

            session.run(
                query,
                customer_id=event.customer_id,
                email=event.email,
                phone_number=event.phone_number,
                first_name=event.person.first_name,
                last_name=event.person.last_name,
                date_of_birth=event.person.date_of_birth,
                ssn=event.person.ssn
            )

    def create_address_node(self, address):
        with self.driver.session() as session:
            session.run(
                "MERGE (a:Address {address_id: $address_id}) "
                "SET a.street_address = $street_address, a.city = $city, a.state = $state, a.zip_code = $zip_code",
                address_id=address.address_id,
                street_address=address.street_address,
                city=address.city,
                state=address.state,
                zip_code=address.zip_code
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

    def create_customer_event_relationship(self, event):
        query = dedent("""\
            MATCH (c:Customer {customer_id: $customer_id})
            CREATE (c)-[:PERFORMS {timestamp: $timestamp}]->(:Event {type: $event_type})
        """)

        with self.driver.session() as session:
            session.run(
                query,
                customer_id=event.customer_id,
                timestamp=event.timestamp,
                event_type=event.event_type
            )

    def create_customer_device_relationship(self, customer_id, device_id, timestamp):
        query = dedent("""\
            MATCH (c:Customer {customer_id: $customer_id})
            MATCH (d:Device {device_id: $device_id})
            MERGE (c)-[r:USES_DEVICE]->(d)
            ON CREATE SET r.since = $timestamp
        """)
        
        with self.driver.session() as session:
            session.run(
                query,
                customer_id=customer_id,
                device_id=device_id,
                timestamp=timestamp
            )

    def create_customer_ip_address_relationship(self, customer_id, ip, timestamp):
        query = dedent("""\
            MATCH (c:Customer {customer_id: $customer_id})
            MATCH (i:IpAddress {ip: $ip})
            MERGE (c)-[r:HAS_IP_ADDRESS]->(i)
            ON CREATE SET r.since = $timestamp
        """)

        with self.driver.session() as session:
            session.run(
                query,
                customer_id=customer_id,
                ip=ip,
                timestamp=timestamp
            )

    def create_customer_address_relationship(self, customer_id, address_id, timestamp):
        query = dedent("""\
            MATCH (c:Customer {customer_id: $customer_id})
            MATCH (a:Address {address_id: $address_id})
            MERGE (c)-[r:RESIDES_AT]->(d)
            ON CREATE SET r.since = $timestamp
        """)
        
        with self.driver.session() as session:
            session.run(
                query,
                customer_id=customer_id,
                address_id=address_id,
                timestamp=timestamp
            )