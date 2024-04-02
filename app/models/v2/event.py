"""
Event models
"""
from typing import Union, Optional
from pydantic import BaseModel, Field
from app.models.v2.base import BaseEnum
from app.models.v2.user import Device, IpAddress
from app.models.v2.customer import Customer
from app.models.v2.application import Application

class CustomerEventType(BaseEnum):
    CUSTOMER_REGISTRATION = "customer_registration"
    CUSTOMER_LOGIN = "customer_login"

class ApplicationEventType(BaseEnum):
    APPLICATION_SUBMISSION = "application_submission"

class Event(BaseModel):
    """
    Zenith Event Model
    """
    uid: str
    type: Union[CustomerEventType, ApplicationEventType]
    timestamp: int
    device: Device = Field(...)
    ip_address: IpAddress = Field(...)
    customer: Customer = Field(...)
    application: Optional[Application] = Field(None)

    class Config:
        title = "Event"
