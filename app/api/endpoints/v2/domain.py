from fastapi import APIRouter
from app.models.v2.foo import Foo # example
from app.models.v2.bar import Bar # example
from app.models.v2 import Event, RiskSignal
from typing import Dict
router = APIRouter()

@router.post("/foo", response_model=None)
def create_foo(foo: Foo):
    return foo

@router.post("/bar", response_model=None)
def create_foo(bar: Bar):
    return bar

@router.post("/event", response_model=None)
def create_foo(event: Dict):
    return event

@router.post("/risk-signal", response_model=None)
def create_foo(risk_signal: Dict):
    return risk_signal