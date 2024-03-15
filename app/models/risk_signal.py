import faust
from app.models import Event
from enum import Enum

class SignalEnum(Enum):
    IP_VELOCITY = 'ip_velocity'
    LOGIN_VELOCITY = 'login_velocity'

class RiskSignal(faust.Record, serializer='json'):
    uid: str
    signal: SignalEnum
    event: Event