# This file contains the Pydantic models for requests and responses in the FastAPI app.

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeviceModel(BaseModel):
    id: str
    user_agent: str

class IpAddressModel(BaseModel):
    id: str
    ipv4: str

class AddressModel(BaseModel):
    id: str
    street: str
    city: str
    state: str
    zip: str

class CustomerModel(BaseModel):
    id: str
    email: Optional[str]
    phone: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[datetime]
    ssn: Optional[str]
    address: Optional[AddressModel]

class EventModel(BaseModel):
    id: str
    type: str
    timestamp: datetime

class CustomerEventModel(EventModel):
    customer: CustomerModel
    device: DeviceModel
    ip_address: IpAddressModel