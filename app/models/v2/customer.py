"""
Customer models
"""
from typing import Optional
from datetime import date
from pydantic import BaseModel, Field
from app.models.v2.address import Address

class Customer(BaseModel):
    """
    Zenith Customer Model
    """
    uid: str
    email: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    date_of_birth: Optional[date] = Field(None)
    ssn: Optional[str] = Field(None)
    address: Optional[Address] = Field(None)
    is_fraud: Optional[bool] = Field(False)
