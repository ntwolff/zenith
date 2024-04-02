"""
IP Address Service
"""

from datetime import datetime
from ._base import BaseService

class IpAddressService(BaseService):
    def mark_as_risky(self, uid: str, reason: str):
        properties = {
            "risky": True,
            "risky_since": datetime.now(),
            "risky_reason": reason
        }
        label = "IpAddress"

        super().upsert(label, "uid", uid, properties)
