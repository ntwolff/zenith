import faust
from pydantic import BaseModel, Field

class DeviceModel(BaseModel):
    id: str = Field(..., description="Device ID")
    user_agent: str = Field(..., min_length=1, description="User agent string")

class Device(faust.Record, serializer='json'):
    id: str
    user_agent: str

    @classmethod
    def from_model(cls, model: DeviceModel):
        return cls(
            id=model.id,
            user_agent=model.user_agent
        )