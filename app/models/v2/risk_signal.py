from pydantic import BaseModel
from app.models.v2.event import Event
from enum import Enum

class RiskSignalType(Enum):
    IP_VELOCITY = 'ip_velocity'
    LOGIN_VELOCITY = 'login_velocity'
    APPLICATION_FRAUD = 'application_fraud'

class RiskSignal(BaseModel):
    uid: str
    type: RiskSignalType
    event: Event