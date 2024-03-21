from app.models.v2.base import AbstractBaseModel
from enum import Enum
from pydantic import Field

class TaskType(Enum):
    LINK_CUSTOMERS_BY_PII = 'link_customers_by_pii'

class GraphTask(AbstractBaseModel):
    uid: str = Field(examples=["123e4567-e89b-12d3-a456-426614174000"])
    task: TaskType
    timestamp: int