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
    address_id: str
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
    event_id: str
    timestamp: datetime
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


# @TODO Create a hashed identifier for the address for use in graph database
# import usaddress
#
# def standardize_address(self, address):
#     return " ".join([address.street, address.city, address.state, address.zip_code, address.country]
#     ).lower()
#
# def hash_address(self, address):
#     standardized_address = self.standardize_address(address)
#     parsed_address = usaddress.tag(standardized_address)[0]
#
#     street_hash = hashlib.sha256(parsed_address.get("AddressNumber", "").encode()).hexdigest()
#     city_hash = hashlib.sha256(parsed_address.get("PlaceName", "").encode()).hexdigest()
#     state_hash = hashlib.sha256(parsed_address.get("StateName", "").encode()).hexdigest()
#     zip_hash = hashlib.sha256(parsed_address.get("ZipCode", "").encode()).hexdigest()
#
#     composite_hash = street_hash + city_hash + state_hash + zip_hash
#     fuzzy_match_hash = composite_hash[:16]
#
#     return fuzzy_match_hash