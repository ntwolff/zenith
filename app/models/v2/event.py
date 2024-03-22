import faust
from app.models.v2.base import BaseEnum
from app.models.v2.device import Device
from app.models.v2.ip_address import IpAddress
from app.models.v2.customer import Customer
from app.models.v2.application import Application
from enum import Enum
from typing import Optional, Union

class CustomerEventType(BaseEnum):
    CUSTOMER_REGISTRATION = "customer_registration"
    CUSTOMER_LOGIN = "customer_login"

class ApplicationEventType(BaseEnum):
    APPLICATION_SUBMISSION = "application_submission"

class Event(faust.Record):
    uid: str
    type: str
    timestamp: int
    device: Optional[Device] = None
    ip_address: Optional[IpAddress] = None
    customer: Optional[Customer] = None
    application: Optional[Application] = None