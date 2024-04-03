from pydantic import BaseModel

class IpInfo(BaseModel):
    ip: str
    city: str = None
    region: str = None
    country: str = None
    loc: str = None
    org: str = None
    postal: str = None
    timezone: str = None