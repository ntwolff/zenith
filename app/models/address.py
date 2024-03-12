import faust

class Address(faust.Record, serializer='json'):
    id: str # Hashed value of the address
    street: str
    city: str
    state: str
    zip: str