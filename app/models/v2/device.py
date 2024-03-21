from app.models.v2.base import AbstractBaseModel

class Device(AbstractBaseModel):
    uid: str
    device_id: str
    user_agent: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "uid": "123e4567-e89b-12d3-a456-426614174000",
                    "device_id": "device12345",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537",
                }
            ]
        }
    }