"""
Event models
"""
from typing import Union, Optional
from pydantic import BaseModel, ConfigDict
import faust
from app.models.v2.base import BaseEnum
from app.models.v2.user import Device, IpAddress
from app.models.v2.customer import Customer
from app.models.v2.application import Application

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
