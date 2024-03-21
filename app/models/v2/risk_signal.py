from app.models.v2.base import AbstractBaseModel
from app.models.v2.event import Event
from enum import Enum
from pydantic import Field

class RiskSignalType(Enum):
    IP_VELOCITY = 'ip_velocity'
    LOGIN_VELOCITY = 'login_velocity'
    APPLICATION_FRAUD = 'application_fraud'

#@record
class RiskSignal(AbstractBaseModel):
    uid: str = Field(examples=["123e4567-e89b-12d3-a456-426614174000"])
    type: RiskSignalType
    event: Event