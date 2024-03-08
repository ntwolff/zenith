from pydantic import BaseModel
 
# TODO fix issues to realize unified schema.
# Only used in api at the moment.

class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str