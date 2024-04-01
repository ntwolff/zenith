from app.stream.faust_app import faust_app
from app.models.v2.admin import GraphTask
from faust.serializers import codecs

class graph_task_serializer(codecs.Codec):
    def _dumps(self, obj: GraphTask) -> bytes:
        return obj.model_dump_json().encode('utf-8')

    def _loads(self, s: bytes) -> GraphTask:
        return GraphTask.parse_raw(s.decode('utf-8'))
    
codecs.register('graph_task_serializer', graph_task_serializer())

graph_management_topic = faust_app.topic('graph_management', value_serializer='graph_task_serializer')