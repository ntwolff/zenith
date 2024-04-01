from pydantic import BaseModel

class Bar(BaseModel):
    uid: str
    age: int