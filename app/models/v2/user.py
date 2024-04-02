"""
User models
"""

from pydantic import BaseModel

class Device(BaseModel):
    uid: str
    device_id: str
    user_agent: str

class IpAddress(BaseModel):
    uid: str
    ipv4: str

