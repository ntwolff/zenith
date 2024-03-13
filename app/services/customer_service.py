from app.models import Customer, Address
from .base_service import BaseService

class CustomerService(BaseService):
    def upsert(self, customer: Customer):
        query = """
            MERGE (c:Customer {customer_id: $id})
            ON CREATE SET c += $properties
            ON MATCH SET c += $properties
        """
        
        # exclude address
        customer_properties = customer.asdict()
        customer_properties.pop("address")
        
        self.db.execute_query(query, id=customer.customer_id, properties=customer_properties)

    def create_relationship(self, customer: Customer, related_obj_key: str, related_obj_value: str, relationship_type: str):
        query = f"""
            MATCH (c:Customer {{customer_id: $customer_id}})
            MATCH (o {{{related_obj_key}: $related_obj_value}})
            MERGE (c)-[r:{relationship_type}]->(o)
        """
        self.db.execute_query(query, customer_id=customer.customer_id, related_obj_value=related_obj_value)

    def mark_as_risky(self, customer_id: str, reason: str):
        query = """
            MATCH (c:Customer {id: $customer_id})
            SET c.risky = True, c.risky_since = datetime(), c.risky_reason = $reason
        """
        self.db.execute_query(query, customer_id=customer_id, reason=reason)

    def link_customers_by_pii(self, pii_type, pii_value):
        query = """
            MATCH (c1:Customer)
            MATCH (c2:Customer)
            WHERE c1 <> c2
            AND c1[$pii_type] = $pii_value
            AND c2[$pii_type] = $pii_value
            MERGE (c1)-[:SHARES_PII {type: $pii_type, value: $pii_value}]-(c2)
        """
        self.db.execute_query(query, pii_type=pii_type, pii_value=pii_value)

    def link_customers_by_address(self, address: Address):
        query = """
            MATCH (c1:Customer)
            MATCH (c2:Customer)
            WHERE c1 <> c2
            AND c1.address.latitude = $latitude
            AND c1.address.longitude = $longitude
            AND c2.address.latitude = $latitude
            AND c2.address.longitude = $longitude
            MERGE (c1)-[:SHARES_PII {type: 'address', value: $address_string}]-(c2)
        """
        self.db.execute_query(query, latitude=address.latitude, longitude=address.longitude, address_string=str(address))