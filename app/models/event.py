"""
Event models
"""
from typing import Union, Optional
from pydantic import BaseModel
from app.models._base import BaseEnum
from app.models.user import Device, IpAddress
from app.models.customer import Customer
from app.models.application import Application

class CustomerEventType(BaseEnum):
    CUSTOMER_REGISTRATION = 'customer_registration'
    CUSTOMER_LOGIN = 'customer_login'

class ApplicationEventType(BaseEnum):
    APPLICATION_SUBMISSION = 'application_submission'

class Event(BaseModel):
    uid: str
    event_type: Union[CustomerEventType, ApplicationEventType, None]
    timestamp: int
    device: Device
    ip_address: IpAddress
    customer: Customer
    application: Optional[Application] = None
