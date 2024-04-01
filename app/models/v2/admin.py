from pydantic import BaseModel
from enum import Enum

class TaskType(str, Enum):
    LINK_CUSTOMERS_BY_PII = 'link_customers_by_pii'

class GraphTask(BaseModel):
    uid: str
    task: TaskType
    timestamp: int