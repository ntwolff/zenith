from app.models.device import Device
from .base_service import BaseService

class DeviceService(BaseService):
    def upsert(self, device: Device):
        query = """
            MERGE (d:Device {id: $id})
            ON CREATE SET d += $properties
            ON MATCH SET d += $properties
        """
        self.db.execute_query(query, id=device.id, properties=device.asdict())