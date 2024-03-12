import faust

class IpAddress(faust.Record, serializer='json'):
    id: str # Hashed value of the IP address
    ipv4: str