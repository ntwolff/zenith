import faust
from enum import Enum

class TaskType(Enum):
    LINK_CUSTOMERS_BY_PII = 'link_customers_by_pii'

class GraphTask(faust.Record):
    uid: str
    task: TaskType
    timestamp: int