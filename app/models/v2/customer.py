"""
Customer models
"""

from typing import Optional
from datetime import date
from pydantic import BaseModel
from app.models.v2.address import Address

class Customer(BaseModel):
    uid: str
    email: Optional[str] = None
    phone: Optional[str]= None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    ssn: Optional[str] = None
    address: Optional[Address] = None
    is_fraud: Optional[bool] = False
