import faust
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

class Application(faust.Record):
    uid: str 
    source: SourceType
    income: Optional[float] = None
    employment_status: Optional[EmploymentType] = None