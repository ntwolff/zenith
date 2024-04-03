import re
from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr, validator, Field
from pydantic_extra_types.phone_numbers import PhoneNumber
from app.models.base import FraudMixin


class Address(FraudMixin, BaseModel):
    uid: str
    street: str
    city: str
    state: str
    zip: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_valid: Optional[bool] = None

    def address_string(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip}"


class Customer(FraudMixin, BaseModel):
    uid: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None # @TODO PhoneNumber isn't agreeing with Faker
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    ssn: Optional[str] = None
    address: Optional[Address] = None
    is_fraud: Optional[bool] = None


    @validator('date_of_birth')
    def date_of_birth_must_be_in_past(cls, v):
        if v is None: #Optional field
            pass
        elif v >= date.today():
            raise ValueError('date_of_birth must be in the past')
        return v

    @validator('ssn')
    def ssn_must_be_properly_formatted(cls, v):
        if v is None: #Optional field
            pass
        # Valid: ###-##-####
        elif not re.match(r'^\d{3}-\d{2}-\d{4}$', v):
            raise ValueError('ssn must be in the format XXX-XX-XXXX')
        return v

    @validator('first_name', 'last_name')
    def names_must_be_of_reasonable_length(cls, v):
        if v is None: #Optional field
            pass
        elif len(v) < 1 or len(v) > 50:
            raise ValueError('name must be between 1 and 50 characters long')
        return v