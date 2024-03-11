import faust
from dataclasses import field
import datetime
from typing import Optional
from uuid import uuid4

#TODO shared model registry between API and event processing

class Device(faust.Record):
    device_id: str
    user_agent: str

class IpAddress(faust.Record):
    ip: str

class Address(faust.Record):
    address_id: str # @TODO Create a hashed identifier for the address for use in graph database
    street_address: str
    city: str
    state: str
    zip_code: str

class Person(faust.Record):
    first_name: str
    last_name: str
    date_of_birth: datetime
    ssn: str
    address: Optional[Address]

class CustomerEvent(faust.Record):
    customer_id: str
    device: Device
    ip_address: IpAddress
    timestamp: datetime
    event_id: str=field(default=uuid4().hex)
    event_type: str=field(default="unknown")

class RegistrationEvent(CustomerEvent):
    email: str
    phone_number: str
    person: Person
    event_type: str=field(default="registration")

class LoginEvent(CustomerEvent):
    event_type: str=field(default="login")

class LogoutEvent(CustomerEvent):
    event_type: str=field(default="logout")