"""
Risk Signal Topic
"""
from app.stream.faust_app import faust_app

risk_signal_topic = faust_app.topic('risk_signal', value_serializer='risk_signal_serializer')
