import faust
from faust import field
import uuid
import datetime
from typing import List, Optional
from shared.schemas import AddressBase

class Address(faust.Record, serializer='json'):
    street: str
    city: str
    state: str
    zip_code: str
    country: str

class Device(faust.Record, serializer='json'):
    device_id: str
    user_agent: str

class IpAddress(faust.Record, serializer='json'):
    ip: str


## ------------------------
## Events
## ------------------------

class Event(faust.Record, abstract=True):
    event_id: str = uuid.uuid4()
    event_timestamp: datetime = datetime.datetime.now()

### CustomerEvents

class CustomerEvent(Event, abstract=True):
    customer_id: str

class CustomerRegistrationEvent(CustomerEvent, serializer='json', validation=True):
    email: str
    phone_number: str
    name: str
    date_of_birth: str
    ssn: str
    address: Address
    device: Device
    ip_address: IpAddress

    @staticmethod
    def validate():
        # Perform validation checks on the event data
        # Raise ValidationError if any checks fail
        pass


# TODO - REFACTOR CustomerRegistrationEvent --> class Registration(CustomerEvent, serializer='json'):...

class LoginEvent(CustomerEvent, serializer='json'):
    pass

class LogOut(CustomerEvent, serializer='json'):
    pass

class PasswordChange(CustomerEvent, serializer='json'):
    pass

### ApplicationEvents

### AccountEvents

### AdminEvents

class EscalationEvent(faust.Record, serializer='json'):
    escalation_reasons: List[str]
    escalation_timestamp: datetime = datetime.datetime.now()
    escalated_event: Event