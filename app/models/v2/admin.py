"""
Administrative models
"""
from pydantic import BaseModel, Field
from app.models.v2.base import BaseEnum

class AdminTaskType(BaseEnum):
    LINK_CUSTOMERS_BY_PII = 'link_customers_by_pii'

class AdminTask(BaseModel):
    """
    Zenith Admin Task Model
    """
    uid: str
    type: AdminTaskType
    timestamp: int
