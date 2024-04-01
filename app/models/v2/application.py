from pydantic import BaseModel
from app.models.v2.base import BaseEnum
from typing import Optional

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
    uid: str 
    source: Optional[SourceType] = None
    income: Optional[float] = None
    employment_status: Optional[EmploymentType] = None