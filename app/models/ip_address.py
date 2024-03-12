import faust
from pydantic import BaseModel, IPvAnyAddress, Field

class IpAddressModel(BaseModel):
    id: str = Field(..., description="Hashed value of the IP address")
    ipv4: IPvAnyAddress = Field(..., description="IP address")

class IpAddress(faust.Record, serializer='json'):
    id: str
    ipv4: str

    @classmethod
    def from_model(cls, model: IpAddressModel):
        return cls(
            id=model.id,
            ipv4=str(model.ipv4)
        )