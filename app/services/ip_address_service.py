from .base_service import BaseService
from datetime import datetime
from app.models.ip_address import IpAddress

class IpAddressService(BaseService):
    def mark_as_risky(self, ip_address_id: str, reason: str):
        properties = {
            "risky": True,
            "risky_since": datetime.now(),
            "risky_reason": reason
        }
        label = "IpAddress"

        super().upsert(label, "uid", ip_address_id, properties)