import faust

class Device(faust.Record, serializer='json'):
    id: str # device id string
    user_agent: str