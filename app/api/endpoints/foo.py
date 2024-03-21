from fastapi import APIRouter
from app.models.foo.foo import Foo
from app.models.foo.factory import RecordFactory

router = APIRouter()

@router.post("/foo", response_model=Foo, summary="Get a Foo by its unique identifier")
def create_foo(foo: Foo):
    foo_record_cls = RecordFactory(Foo).get_record_class()
    
    print(foo_record_cls(this=foo))
    
    # topic.send(value=foo_record_cls(this=foo)
    return foo