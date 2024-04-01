# from faust import Record
# from pydantic import BaseModel, Field
# from typing import Optional
# from enum import Enum

# class SourceEnum(str, Enum):
#     CREDITKARMA = "creditkarma"
#     LENDINGTREE = "lendingtree"
#     EXPERIAN = "experian"
#     MAIL = "mail"
#     ORGANIC = "organic"
#     OTHER = "other"

# class EmploymentStatusEnum(str, Enum):
#     EMPLOYED = "employed"
#     UNEMPLOYED = "unemployed"
#     STUDENT = "student"
#     RETIRED = "retired"
#     OTHER = "other"

# class ApplicationModel(BaseModel):
#     uid: str = Field(..., description="Unique identifier of the object")
#     application_id: str = Field(..., description="Application identifier")
#     source: SourceEnum = Field(..., description="Application source")
#     income: Optional[float] = Field(None, description="Annual income")
#     employment_status: Optional[str] = Field(None, description="Employment status")

# class Application(Record, serializer='json'):
#     uid: str
#     application_id: str
#     source: SourceEnum
#     income: Optional[float]
#     employment_status: Optional[EmploymentStatusEnum]

#     @classmethod
#     def from_model(cls, model: ApplicationModel):
#         return cls(
#             uid=model.application_id,
#             application_id=model.application_id,
#             source=model.source,
#             income=model.income,
#             employment_status=model.employment_status
#         )