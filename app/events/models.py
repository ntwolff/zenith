import faust

class Event(faust.Record):
    pass

class CustomerRegistrationEvent(Event):
    customer_id: str
    email: str
    phone_number: str
    # ... other fields

class LoginEvent(Event):
    customer_id: str
    timestamp: float
    # ... other fields