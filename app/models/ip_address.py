# import faust
# from pydantic import BaseModel, IPvAnyAddress, Field

# class IpAddressModel(BaseModel):
#     uid: str = Field(..., description="Unique identifier of the object")
#     ip_address_id: str = Field(..., description="Hashed value of the IP address")
#     ipv4: IPvAnyAddress = Field(..., description="IP address")

# class IpAddress(faust.Record, serializer='json'):
#     uid: str
#     ip_address_id: str
#     ipv4: str

#     @classmethod
#     def from_model(cls, model: IpAddressModel):
#         return cls(
#             uid=model.uid,
#             ip_address_id=model.ip_address_id,
#             ipv4=str(model.ipv4)
#         )