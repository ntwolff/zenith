from app.models.v2.base import AbstractBaseModel
from app.models.v2.address import Address
from pydantic import Field, EmailStr, validator
from typing import Optional
from datetime import datetime

class Customer(AbstractBaseModel):
    uid: str = Field(examples=["123e4567-e89b-12d3-a456-426614174000"])
    email: EmailStr = Field(examples=["jane.doe@example.com"])
    phone: Optional[str]= Field(examples=["123-456-7890"])
    first_name: Optional[str] = Field(examples=["Jane"])
    last_name: Optional[str] = Field(examples=["Doe"])
    date_of_birth: Optional[datetime] = Field(examples=["1980-01-01"])
    ssn: Optional[str] = Field(examples=["123-45-6789"])
    address: Optional[Address]
    is_fraud: Optional[bool] = Field(False)

    @validator("date_of_birth")
    def datetime_to_string(cls, v):
        return v.isoformat()