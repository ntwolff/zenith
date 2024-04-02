"""
Administrative Task Topic
"""

from faust.serializers import codecs
from app.stream.faust_app import faust_app
from app.models.v2 import AdminTask

class AdminTaskSerializer(codecs.Codec):
    def _dumps(self, s: AdminTask) -> bytes:
        return s.model_dump_json().encode('utf-8')

    def _loads(self, s: bytes) -> AdminTask:
        return AdminTask.parse_raw(s.decode('utf-8'))

codecs.register('admin_task_serializer', AdminTaskSerializer())

admin_task_topic = faust_app.topic('admin_task', value_serializer='admin_task_serializer')
