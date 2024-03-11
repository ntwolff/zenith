from pydantic import BaseModel

class DeviceModel(BaseModel):
    device_id: str
    user_agent: str

class IpAddressModel(BaseModel):
    ip: str

class CustomerRegistrationEventModel(BaseModel):
    customer_id: str
    email: str
    phone_number: str
    device: DeviceModel
    ip_address: IpAddressModel
    # Add other fields as needed

class LoginEventModel(BaseModel):
    customer_id: str
    timestamp: float
    device: DeviceModel
    ip_address: IpAddressModel
    # Add other fields as needed