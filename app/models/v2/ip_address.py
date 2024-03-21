from app.models.v2.base import AbstractBaseModel
from pydantic import IPvAnyAddress

class IpAddress(AbstractBaseModel):
    uid: str
    ipv4: IPvAnyAddress

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "uid": "123e4567-e89b-12d3-a456-426614174000",
                    "ipv4": "192.168.1.1",
                }
            ]
        }
    }