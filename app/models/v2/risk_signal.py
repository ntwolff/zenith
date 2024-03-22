import faust
from app.models.v2.event import Event
from enum import Enum

class RiskSignalType(Enum):
    IP_VELOCITY = 'ip_velocity'
    LOGIN_VELOCITY = 'login_velocity'
    APPLICATION_FRAUD = 'application_fraud'

#@record
class RiskSignal(faust.Record):
    uid: str
    type: RiskSignalType
    event: Event