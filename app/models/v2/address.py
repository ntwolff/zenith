from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    uid: str
    street: str
    city: str
    state: str
    zip: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_valid: Optional[bool] = False
    validation_id: Optional[str] = None

    def address_string(cls):
        return f"{cls.street}, {cls.city}, {cls.state} {cls.zip}"