from app.stream.faust_app import faust_app
from app.models.v2 import RiskSignal

risk_signal_topic = faust_app.topic('risk_signal', value_type=RiskSignal)