from fastapi import APIRouter
from app.models.foo import FooModel, FooRecord

router = APIRouter()

@router.post("/foo", response_model=FooModel, summary="Get a Foo by its unique identifier")
def create_foo(foo: FooModel):
    record = FooRecord(this=foo)
    
    print(record)
    
    return foo