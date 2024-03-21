# app/stream/codec_registry.py

from app.models.foo.factory import RecordFactory
from app.models.foo.foo import Foo
from app.models.foo.bar import Bar
# Import other model classes as needed

foo_factory = RecordFactory(Foo)
bar_factory = RecordFactory(Bar)
# Create factories for other model classes as needed

def foo_codec():
    return foo_factory.get_codec()

def bar_codec():
    return bar_factory.get_codec()

# Define codec functions for other model classes as needed