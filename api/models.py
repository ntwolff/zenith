from pydantic import BaseModel
from shared.schemas import AddressBase
from typing import List

## /customers/{id}

class Address(AddressBase):
    pass

class Device(BaseModel):
    device_id: str
    user_agent: str

class IpAddress(BaseModel):
    ip: str

class CustomerRegisteredEvent(BaseModel):
    customer_id: str
    email: str
    phone_number: str
    name: str
    date_of_birth: str
    ssn: str
    address: Address
    device: Device
    ip_address: IpAddress
    timestamp: float

## /customers/{id}/analytics
    
class SimilarCustomer(BaseModel):
    similar_customer_id: str

class CustomerAnalytics(BaseModel):
    similar_customers: List[SimilarCustomer]