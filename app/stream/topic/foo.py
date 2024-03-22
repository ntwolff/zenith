from app.stream.faust_app import faust_app
from app.models.v2.foo import Foo
from faust.serializers import codecs

class foo_serializer(codecs.Codec):
    def _dumps(self, obj: Foo) -> bytes:
        return obj.model_dump_json().encode('utf-8')

    def _loads(self, s: bytes) -> Foo:
        return Foo.parse_raw(s.decode('utf-8'))
    
codecs.register('foo_serializer', foo_serializer())

foo_topic = faust_app.topic('foo', value_serializer='foo_serializer')