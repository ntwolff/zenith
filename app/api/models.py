from pydantic import BaseModel
from typing import Optional
from dataclasses import field
from datetime import datetime
from uuid import uuid4

#TODO shared model registry between API and event processing

class DeviceModel(BaseModel):
    device_id: str
    user_agent: str

class IpAddressModel(BaseModel):
    ip: str

class AddressModel(BaseModel):
    address_id: str
    street_address: str
    city: str
    state: str
    zip_code: str

class PersonModel(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: datetime
    ssn: str
    address: Optional[AddressModel]

class CustomerEventModel(BaseModel):
    customer_id: str
    device: DeviceModel
    ip_address: IpAddressModel
    event_id: str
    timestamp: datetime
    event_type: str

class RegistrationEventModel(CustomerEventModel):
    email: str
    phone_number: str
    person: PersonModel
    event_type: str

class LoginEventModel(CustomerEventModel):
    event_type: str