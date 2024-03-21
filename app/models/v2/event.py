from app.models.v2.base import AbstractBaseModel
from app.models.v2.device import Device
from app.models.v2.ip_address import IpAddress
from app.models.v2.customer import Customer
from app.models.v2.application import Application
from enum import Enum
from pydantic import Field

class EventType(Enum):
    CUSTOMER_REGISTRATION = "customer_registration"
    CUSTOMER_LOGIN = "customer_login"
    APP_SUBMISSION = "app_submission"

class Event(AbstractBaseModel):
    uid: str = Field(examples=["123e4567-e89b-12d3-a456-426614174000"])
    type: EventType
    timestamp: int
    device: Device
    ip_address: IpAddress

#@record
class CustomerEvent(Event):
    customer: Customer

#@record
class ApplicationEvent(Event):
    customer: Customer
    application: Application