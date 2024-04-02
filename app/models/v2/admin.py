"""
Administrative models
"""

from pydantic import BaseModel
from app.models.v2.base import BaseEnum

class AdminTaskType(BaseEnum):
    LINK_CUSTOMERS_BY_PII = 'link_customers_by_pii'

class AdminTask(BaseModel):
    uid: str
    type: AdminTaskType
    timestamp: int
