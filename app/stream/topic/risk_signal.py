from app.stream.faust_app import faust_app
from app.models.v2 import RiskSignal
from faust.serializers import codecs

class risk_signal_serializer(codecs.Codec):
    def _dumps(self, obj: RiskSignal) -> bytes:
        return obj.model_dump_json().encode('utf-8')

    def _loads(self, s: bytes) -> RiskSignal:
        return RiskSignal.parse_raw(s.decode('utf-8'))
    
codecs.register('risk_signal_serializer', risk_signal_serializer())

risk_signal_topic = faust_app.topic('risk_signal', value_serializer='risk_signal_serializer')