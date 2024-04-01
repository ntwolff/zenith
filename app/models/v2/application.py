from pydantic import BaseModel
from typing import Optional
from enum import Enum

class SourceType(str, Enum):
    CREDITKARMA = "creditkarma"
    LENDINGTREE = "lendingtree"
    EXPERIAN = "experian"
    MAIL = "mail"
    ORGANIC = "organic"
    OTHER = "other"

class EmploymentType(str, Enum):
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