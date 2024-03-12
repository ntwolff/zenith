import faust
from app.models.address import Address
from datetime import datetime
from typing import Optional

class Customer(faust.Record, serializer='json'):
    id: str
    email: Optional[str]
    phone: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[datetime]
    ssn: Optional[str]
    address: Optional[Address]
    last_active_at: Optional[datetime]