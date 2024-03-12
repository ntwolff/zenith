import faust
from pydantic import BaseModel, Field

class AddressModel(BaseModel):
    id: str = Field(..., description="Hashed value of the address")
    street: str = Field(..., min_length=1, max_length=255, description="Street address")
    city: str = Field(..., min_length=1, max_length=255, description="City")
    state: str = Field(..., min_length=2, max_length=2, description="State abbreviation")
    zip: str = Field(..., pattern=r'^\d{5}(?:[-\s]\d{4})?$', description="ZIP code")

class Address(faust.Record, serializer='json'):
    id: str
    street: str
    city: str
    state: str
    zip: str

    @classmethod
    def from_model(cls, model: AddressModel):
        return cls(
            id=model.id,
            street=model.street,
            city=model.city,
            state=model.state,
            zip=model.zip
        )