from .base_service import BaseService
from app.models.ip_address import IpAddress

class IpAddressService(BaseService):
    def upsert(self, ip_address: IpAddress):
        query = """
            MERGE (i:IpAddress {id: $id})
            ON CREATE SET i += $properties
            ON MATCH SET i += $properties
        """
        self.db.execute_query(query, id=ip_address.id, properties=ip_address.asdict())

    def mark_as_risky(self, ip_address_id: str, reason: str):
        query = """
            MATCH (i:IpAddress {id: $ip_address_id})
            SET i.risky = True, i.risky_since = datetime(), i.risky_reason = $reason
        """
        self.db.execute_query(query, ip_address_id=ip_address_id, reason=reason)