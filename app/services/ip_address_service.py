"""
Ip Address Service
"""

from .base_service import BaseService
from datetime import datetime

class IpAddressService(BaseService):
    def mark_as_risky(self, uid: str, reason: str):
        properties = {
            "risky": True,
            "risky_since": datetime.now(),
            "risky_reason": reason
        }
        label = "IpAddress"

        super().upsert(label, "uid", uid, properties)