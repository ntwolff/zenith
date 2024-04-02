"""
Application models
"""
from typing import Optional
from pydantic import BaseModel, Field
from app.models.v2.base import BaseEnum

class SourceType(BaseEnum):
    CREDITKARMA = "creditkarma"
    LENDINGTREE = "lendingtree"
    EXPERIAN = "experian"
    MAIL = "mail"
    ORGANIC = "organic"
    OTHER = "other"

class EmploymentType(BaseEnum):
    EMPLOYED = "employed"
    UNEMPLOYED = "unemployed"
    STUDENT = "student"
    RETIRED = "retired"
    OTHER = "other"

class Application(BaseModel):
    """
    Zenith Application Model
    """
    uid: str
    source: Optional[SourceType] = None
    income: Optional[float] = None
    employment_status: Optional[EmploymentType] = None
