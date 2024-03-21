from pydantic import BaseModel, ConfigDict
import abc

class ZenithBaseModel(BaseModel, abc.ABC):
    model_config = ConfigDict(arbitrary_types_allowed = True)