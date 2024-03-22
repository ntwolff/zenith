import faust
from typing import Optional

class Address(faust.Record):
    uid: str
    street: str
    city: str
    state: str
    zip: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    _is_valid: Optional[bool] = False
    _validation_id: Optional[str] = None

    def address_string(cls):
        return f"{cls.street}, {cls.city}, {cls.state} {cls.zip}"