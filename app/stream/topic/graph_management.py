from app.stream.faust_app import faust_app
from app.models.v2.admin import GraphTask

graph_management_topic = faust_app.topic('graph_management', value_type=GraphTask)