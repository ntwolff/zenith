import faust

class IpAddress(faust.Record):
    uid: str
    ipv4: str