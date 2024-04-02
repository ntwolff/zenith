"""
Fraud models
"""
from pydantic import BaseModel, Field
from app.models.event import Event
from app.models._base import BaseEnum

class RiskSignalType(BaseEnum):
    IP_VELOCITY = 'ip_velocity'
    LOGIN_VELOCITY = 'login_velocity'
    APPLICATION_FRAUD = 'application_fraud'

class RiskSignal(BaseModel):
    uid: str
    signal_type: RiskSignalType
    event: Event = Field(...)
