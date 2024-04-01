# import faust
# from pydantic import BaseModel, Field
# from app.models.customer import CustomerModel, Customer
# from app.models.device import DeviceModel, Device
# from app.models.application import ApplicationModel, Application
# from app.models.ip_address import IpAddressModel, IpAddress
# from enum import Enum
# from typing import Union

# class CustomerEventTypeEnum(str, Enum):
#     REGISTRATION = "registration"
#     LOGIN = "login"

# class ApplicationEventTypeEnum(str, Enum):
#     SUBMISSION = "submission"

# class EventModel(BaseModel):
#     uid: str = Field(..., description="Unique identifier of the object")
#     event_id: str = Field(..., description="Unique identifier of the event")
#     type: Union[CustomerEventTypeEnum, ApplicationEventTypeEnum] = Field(..., description="Event type")
#     timestamp: int = Field(..., description="Event timestamp")
#     device: DeviceModel = Field(..., description="Device")
#     ip_address: IpAddressModel = Field(..., description="IP address")

# class CustomerEventModel(EventModel):
#     customer: CustomerModel = Field(..., description="Customer")

# class ApplicationEventModel(EventModel):
#     customer: CustomerModel = Field(..., description="Customer")
#     application: ApplicationModel = Field(..., description="Application")

# class Event(faust.Record, abstract=True, serializer='json'):
#     uid: str
#     event_id: str
#     type: str
#     timestamp: int
#     device: Device
#     ip_address: IpAddress

# class CustomerEvent(Event, serializer='json'):
#     customer: Customer

#     @classmethod
#     def from_model(cls, model: CustomerEventModel):
#         return cls(
#             uid=model.event_id,
#             event_id=model.event_id,
#             type=model.type.value,
#             timestamp=model.timestamp,
#             customer=Customer.from_model(model.customer),
#             device=Device.from_model(model.device),
#             ip_address=IpAddress.from_model(model.ip_address)
#         )

# class ApplicationEvent(Event, serializer='json'):
#     customer: Customer
#     application: Application

#     @classmethod
#     def from_model(cls, model: ApplicationEventModel):
#         return cls(
#             uid=model.event_id,
#             event_id=model.event_id,
#             type=model.type.value,
#             timestamp=model.timestamp,
#             customer=Customer.from_model(model.customer),
#             application=Application.from_model(model.application),
#             device=Device.from_model(model.device),
#             ip_address=IpAddress.from_model(model.ip_address)
#         )