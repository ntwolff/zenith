from pydantic import BaseModel
from app.models.v2.base import BaseEnum
from app.models.v2.device import Device
from app.models.v2.ip_address import IpAddress
from app.models.v2.customer import Customer
from app.models.v2.application import Application
from typing import Optional

class CustomerEventType(BaseEnum):
    CUSTOMER_REGISTRATION = "customer_registration"
    CUSTOMER_LOGIN = "customer_login"

class ApplicationEventType(BaseEnum):
    APPLICATION_SUBMISSION = "application_submission"

class Event(BaseModel):
    uid: str
    type: str
    timestamp: int
    device: Device
    ip_address: IpAddress
    customer: Customer
    application: Optional[Application] = None