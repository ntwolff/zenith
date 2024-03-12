from .base_service import BaseService
from app.models.address import Address

class AddressService(BaseService):
    def upsert(self, address: Address):
        query = """
            MERGE (a:Address {id: $id})
            ON CREATE SET a += $properties
            ON MATCH SET a += $properties
        """
        self.db.execute_query(query, id=address.id, properties=address.asdict())