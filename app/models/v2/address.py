"""
Address models
"""
from typing import Optional
from pydantic import BaseModel, Field

class Address(BaseModel):
    uid: str
    street: str
    city: str
    state: str
    zip: str
    latitude: Optional[float] = Field(None)
    longitude: Optional[float] = Field(None)
    is_valid: Optional[bool] = Field(False)
    validation_id: Optional[str] = Field(None)

    def address_string(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip}"
