from app.stream.faust_app import faust_app
from app.models.v2 import Event
from faust.serializers import codecs

class event_serializer(codecs.Codec):
    def _dumps(self, obj: Event) -> bytes:
        return obj.model_dump_json().encode('utf-8')

    def _loads(self, s: bytes) -> Event:
        return Event.parse_raw(s.decode('utf-8'))
    
codecs.register('event_serializer', event_serializer())

event_topic = faust_app.topic('event', value_serializer='event_serializer')