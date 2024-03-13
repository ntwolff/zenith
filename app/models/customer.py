import faust
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .address import AddressModel, Address

class CustomerModel(BaseModel):
    customer_id: str = Field(..., description="Customer ID")
    email: str = Field(..., description="Email address")
    phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$', description="Phone number")
    first_name: Optional[str] = Field(None, min_length=1, max_length=255, description="First name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=255, description="Last name")
    date_of_birth: Optional[datetime] = Field(None, description="Date of birth")
    ssn: Optional[str] = Field(None, pattern=r'^\d{3}-\d{2}-\d{4}$', description="Social Security Number")
    address: Optional[AddressModel] = Field(None, description="Address")
    is_fraud: Optional[bool] = Field(False, description="Marked as fraud")
    last_active_at: Optional[datetime] = Field(None, description="Last customer event timestamp")

class Customer(faust.Record, serializer='json'):
    customer_id: str
    email: Optional[str]
    phone: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[datetime]
    ssn: Optional[str]
    address: Optional[Address]
    is_fraud: Optional[bool]
    last_active_at: Optional[datetime]

    @classmethod
    def from_model(cls, model: CustomerModel):
        return cls(
            customer_id=model.customer_id,
            email=model.email,
            phone=model.phone,
            first_name=model.first_name,
            last_name=model.last_name,
            date_of_birth=model.date_of_birth,
            ssn=model.ssn,
            address=Address.from_model(model.address) if model.address else None,
            is_fraud=model.is_fraud
        )