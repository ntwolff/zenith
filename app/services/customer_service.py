from app.models.customer import Customer
from .base_service import BaseService

class CustomerService(BaseService):
    def upsert(self, customer: Customer):
        query = """
            MERGE (c:Customer {id: $id})
            ON CREATE SET c += $properties
            ON MATCH SET c += $properties
        """
        
        # exclude address
        customer_properties = customer.asdict()
        customer_properties.pop("address")
        
        self.db.execute_query(query, id=customer.id, properties=customer_properties)

    def create_relationship(self, customer: Customer, related_object, relationship_type: str):
        query = f"""
            MATCH (c:Customer {{id: $customer_id}})
            MATCH (o {{id: $object_id}})
            MERGE (c)-[r:{relationship_type}]->(o)
        """
        self.db.execute_query(query, customer_id=customer.id, object_id=related_object.id)

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