from pydantic import BaseModel
from app.models.v2.bar import Bar

class Foo(BaseModel):
    uid: str
    name: str
    bar: Bar