from typing import Union, Optional
from datetime import datetime
from pydantic import BaseModel, validator
from app.models.customer import Customer
from app.models.application import Application
from app.models.base import FraudMixin, BaseEnum


class CustomerEventType(BaseEnum):
    CUSTOMER_REGISTRATION = 'customer_registration'
    CUSTOMER_LOGIN = 'customer_login'


class ApplicationEventType(BaseEnum):
    APPLICATION_SUBMISSION = 'application_submission'


class Device(FraudMixin, BaseModel):
    uid: str
    device_id: str
    user_agent: str


class IpAddress(FraudMixin, BaseModel):
    uid: str
    ipv4: str


class Event(FraudMixin, BaseModel):
    uid: str
    event_type: Union[CustomerEventType, ApplicationEventType, None]
    timestamp: int
    device: Device
    ip_address: IpAddress
    customer: Customer
    application: Optional[Application] = None

    @validator('timestamp')
    def timestamp_valid(cls, timestamp):
        assert datetime.fromtimestamp(timestamp) < datetime.now(), 'Event timestamp cannot be in the future'
        return timestamp
