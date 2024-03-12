import faust
from app.models.customer import Customer
from app.models.device import Device
from app.models.ip_address import IpAddress
from dataclasses import field
from datetime import datetime
from uuid import uuid4

class Event(faust.Record, abstract=True, serializer='json'):
    id: str = field(default=str(uuid4()))
    type: str = field(default="unknown")
    timestamp: datetime = field(default=datetime.now())

class CustomerEvent(Event, serializer='json'):
    customer: Customer
    device: Device
    ip_address: IpAddress