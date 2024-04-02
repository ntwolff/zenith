"""
Administrative Task Topic
"""
from app.stream.faust_app import faust_app

admin_task_topic = faust_app.topic('admin_task', value_serializer='admin_task_serializer')
