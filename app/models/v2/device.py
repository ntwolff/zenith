import faust

class Device(faust.Record):
    uid: str
    device_id: str
    user_agent: str