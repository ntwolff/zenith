"""
Event models
"""
from typing import Union, Optional
from pydantic import BaseModel, Field, ConfigDict
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
    """
    Zenith Event Model
    """
    model_config = ConfigDict(
        title='Event', 
        extra='allow', 
        use_enum_values=True, 
        arbitrary_types_allowed=True)

    uid: str
    type: Union[CustomerEventType, ApplicationEventType, None] = Field(..., alias='event_type')
    timestamp: int
    device: Device
    ip_address: IpAddress
    customer: Customer
    application: Optional[Application] = None
