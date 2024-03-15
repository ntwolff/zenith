import faust
from enum import Enum

class TaskEnum(Enum):
    LINK_CUSTOMERS_BY_PII = 'link_customers_by_pii'

class GraphTask(faust.Record, serializer='json'):
    uid: str
    task: TaskEnum
    timestamp: int