"""
Fraud models
"""
from pydantic import BaseModel, Field
from app.models.v2.event import Event
from app.models.v2.base import BaseEnum

class RiskSignalType(BaseEnum):
    IP_VELOCITY = 'ip_velocity'
    LOGIN_VELOCITY = 'login_velocity'
    APPLICATION_FRAUD = 'application_fraud'

class RiskSignal(BaseModel):
    uid: str
    type: RiskSignalType
    event: Event = Field(...)
