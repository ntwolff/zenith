import faust
from pydantic import BaseModel, Field
from typing import Optional

class AddressModel(BaseModel):
    address_id: str = Field(..., description="Hashed value of the address")
    street: str = Field(..., min_length=1, max_length=255, description="Street address")
    city: str = Field(..., min_length=1, max_length=255, description="City")
    state: str = Field(..., min_length=2, max_length=2, description="State abbreviation")
    zip: str = Field(..., pattern=r'^\d{5}(?:[-\s]\d{4})?$', description="ZIP code")
    latitude: Optional[float] = Field(None, description="Latitude of the address")
    longitude: Optional[float] = Field(None, description="Longitude of the address")
    is_valid: Optional[bool] = Field(None, description="Indicates if the address is valid")
    validation_id: Optional[str] = Field(None, description="Google Maps response identifier")

class Address(faust.Record, serializer='json'):
    address_id: str
    street: str
    city: str
    state: str
    zip: str
    latitude: Optional[float]
    longitude: Optional[float]
    is_valid: Optional[bool]
    validation_id: Optional[str]

    @classmethod
    def from_model(cls, model: AddressModel):
        return cls(
            address_id=model.address_id,
            street=model.street,
            city=model.city,
            state=model.state,
            zip=model.zip,
            latitude=model.latitude,
            longitude=model.longitude,
            is_valid=model.is_valid
        )