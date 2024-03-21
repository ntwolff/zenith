from app.models.v2.base import AbstractBaseModel
from typing import Optional

class Address(AbstractBaseModel):
    uid: str
    street: str
    city: str
    state: str
    zip: str
    latitude: Optional[float]
    longitude: Optional[float]
    _is_valid: Optional[bool]
    _validation_id: Optional[str]
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "uid": "123e4567-e89b-12d3-a456-426614174000",
                    "street": "123 Main St",
                    "city": "Springfield",
                    "state": "IL",
                    "zip": "62701",
                    "latitude": 39.7817,
                    "longitude": -89.6501
                }
            ]
        }
    }

    def address_string(cls):
        return f"{cls.street}, {cls.city}, {cls.state} {cls.zip}"