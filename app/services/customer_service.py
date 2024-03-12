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