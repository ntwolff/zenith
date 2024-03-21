from app.models.v2.base import AbstractBaseModel
from typing import Optional
from enum import Enum
from pydantic import Field

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

class Application(AbstractBaseModel):
    uid: str = Field(examples=["123e4567-e89b-12d3-a456-426614174000"])
    source: SourceType
    income: Optional[float]
    employment_status: Optional[EmploymentType]