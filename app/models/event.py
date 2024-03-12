import faust
from pydantic import BaseModel, Field
from .customer import CustomerModel, Customer
from .device import DeviceModel, Device
from .ip_address import IpAddressModel, IpAddress

class EventModel(BaseModel):
    id: str = Field(..., description="Event ID")
    type: str = Field(..., description="Event type")
    timestamp: int = Field(..., description="Event timestamp")

class CustomerEventModel(EventModel):
    customer: CustomerModel = Field(..., description="Customer")
    device: DeviceModel = Field(..., description="Device")
    ip_address: IpAddressModel = Field(..., description="IP address")

class Event(faust.Record, abstract=True, serializer='json'):
    id: str
    type: str
    timestamp: int

class CustomerEvent(Event, serializer='json'):
    customer: Customer
    device: Device
    ip_address: IpAddress

    @classmethod
    def from_model(cls, model: CustomerEventModel):
        return cls(
            id=model.id,
            type=model.type,
            timestamp=model.timestamp,
            customer=Customer.from_model(model.customer),
            device=Device.from_model(model.device),
            ip_address=IpAddress.from_model(model.ip_address)
        )