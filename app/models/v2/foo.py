from pydantic import BaseModel

class Foo(BaseModel):
    uid: str
    name: str