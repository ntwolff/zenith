import faust
from pydantic import BaseModel

class Bar(BaseModel):
    uid: str
    name: str
    age: int