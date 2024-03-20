from app.faust.app import faust_app
from app.models import RiskSignal

risk_signal_topic = faust_app.topic('risk_signal', value_type=RiskSignal)