"""
Risk Signal Codec
"""
import logging
from faust.serializers import codecs
from schema_registry.client import SchemaRegistryClient, schema
from app.config.settings import settings
from app.models.v2 import RiskSignal

class RiskSignalSerializer(codecs.Codec):
    def __init__(self):
        self.kafka_registry_schema_id = self._generate_json_schema_codec()
        super().__init__()

    def _dumps(self, s: RiskSignal) -> bytes:
        return s.model_dump_json().encode('utf-8')

    def _loads(self, s: bytes) -> RiskSignal:
        return RiskSignal.parse_raw(s.decode('utf-8'))
    
    def _generate_json_schema_codec(self):
        logging.info(RiskSignal.schema_json(indent=2))
        risk_signal_schema = schema.JsonSchema(RiskSignal.schema_json())
        client = SchemaRegistryClient(url=settings.kafka_schema_registry_url)
        schema_id = client.register("risk-signals", risk_signal_schema, schema_type="JSON")
        return schema_id
