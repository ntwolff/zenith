import faust

class Device(faust.Record):
    device_id: str
    user_agent: str

class IpAddress(faust.Record):
    ip: str

class Event(faust.Record):
    device: Device
    ip_address: IpAddress

class CustomerRegistrationEvent(Event):
    customer_id: str
    email: str
    phone_number: str
    # ... other fields

class LoginEvent(Event):
    customer_id: str
    timestamp: float
    # ... other fields