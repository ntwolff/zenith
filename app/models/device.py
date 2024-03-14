from faust import Record
from pydantic import BaseModel, Field

class DeviceModel(BaseModel):
    uid: str = Field(..., description="Unique identifier of the object")
    device_id: str = Field(..., description="Device ID")
    user_agent: str = Field(..., min_length=1, description="User agent string")

class Device(Record, serializer='json'):
    uid: str
    device_id: str
    user_agent: str

    @classmethod
    def from_model(cls, model: DeviceModel):
        return cls(
            uid=model.device_id,
            device_id=model.device_id,
            user_agent=model.user_agent
        )