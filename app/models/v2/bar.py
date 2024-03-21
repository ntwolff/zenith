from app.models.v2.base import AbstractBaseModel

class Bar(AbstractBaseModel):
    uid: str
    name: str
    age: int