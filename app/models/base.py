import uuid
from datetime import datetime
from enum import Enum, EnumMeta
from typing import Optional
from pydantic import BaseModel, Field

class BaseEntity(BaseModel):
    uid: str = Field(default_factory=uuid.uuid4, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item) # pylint: disable=no-value-for-parameter
        except ValueError:
            return False
        return True

class BaseEnum(str, Enum, metaclass=MetaEnum):
    pass # pylint: disable=unnecessary-pass


class EntityType(str, Enum):
    CUSTOMER = 'customer'
    APPLICATION = 'application'
    IP_ADDRESS = 'ip_address'
    DEVICE = 'device'
    PHONE_NUMBER = 'phone_number'
    ADDRESS = 'address'
    SSN = 'ssn'

class FraudStatus(str, Enum):
    UNKNOWN = 'unknown'
    SUSPECTED = 'suspected'
    CONFIRMED = 'confirmed'
    CLEARED = 'cleared'

class FraudMixin(BaseModel):
    fraud_status: Optional[FraudStatus] = None
    fraud_reason: Optional[str] = None
    entity_insights: Optional[dict] = None
