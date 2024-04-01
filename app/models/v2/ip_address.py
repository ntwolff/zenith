from pydantic import BaseModel

class IpAddress(BaseModel):
    uid: str
    ipv4: str