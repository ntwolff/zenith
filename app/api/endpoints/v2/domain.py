from fastapi import APIRouter
from app.models.v2.base import RecordFactory
from app.models.v2.foo import Foo # example
from app.models.v2.bar import Bar # example
from app.models.v2 import CustomerEvent, ApplicationEvent, RiskSignal

router = APIRouter()

@router.post("/foo", response_model=Foo)
def create_foo(foo: Foo):
    cls = RecordFactory(Foo).get_record_class()
    print(cls(this=foo))
    return foo

@router.post("/bar", response_model=Bar)
def create_foo(bar: Bar):
    cls = RecordFactory(Bar).get_record_class()
    print(cls(this=bar))
    return bar

@router.post("/events/customer", response_model=CustomerEvent)
def create_foo(customer_event: CustomerEvent):
    cls = RecordFactory(CustomerEvent).get_record_class()
    print(cls(this=customer_event))
    return customer_event

@router.post("/events/application", response_model=ApplicationEvent)
def create_foo(application_event: ApplicationEvent):
    cls = RecordFactory(ApplicationEvent).get_record_class()
    print(cls(this=application_event))
    return application_event

@router.post("/events/risk-signal", response_model=RiskSignal)
def create_foo(risk_signal: RiskSignal):
    cls = RecordFactory(RiskSignal).get_record_class()
    print(cls(this=risk_signal))
    return risk_signal