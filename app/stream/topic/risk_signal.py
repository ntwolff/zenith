"""
Risk Signal Topic
"""

from faust.serializers import codecs
from app.stream.faust_app import faust_app
from app.models.v2 import RiskSignal

class RiskSignalSerializer(codecs.Codec):
    def _dumps(self, s: RiskSignal) -> bytes:
        return s.model_dump_json().encode('utf-8')

    def _loads(self, s: bytes) -> RiskSignal:
        return RiskSignal.parse_raw(s.decode('utf-8'))

codecs.register('risk_signal_serializer', RiskSignalSerializer())

risk_signal_topic = faust_app.topic('risk_signal', value_serializer='risk_signal_serializer')
