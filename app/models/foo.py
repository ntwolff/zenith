import faust
from typing import Any, Type
from pydantic import BaseModel, ConfigDict, GetCoreSchemaHandler, TypeAdapter
from pydantic_core import CoreSchema, core_schema
import abc
from typing import Optional

class ZenithBaseModel(BaseModel, abc.ABC):
    model_config = ConfigDict(arbitrary_types_allowed = True)

class ZenithBaseRecord(faust.Record, abstract=True):
    this: ZenithBaseModel

    @classmethod
    def __get_pydantic_core_schema__(
        self, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        #assert source is ZenithBaseRecord
        if not source.this:
            raise ValueError('The Record must have a field named this')
        #assert source is ZenithBaseModel
        schema = handler(source.this.type)
        return core_schema.typed_dict_schema(
            {
                'this': core_schema.typed_dict_field(core_schema.model_ser_schema(source.this.type, schema)),
            },
        )

class FooModel(ZenithBaseModel):
    uid: str
    name: str

class FooRecord(ZenithBaseRecord, serializer='json_foos'):
    this: FooModel

# class BarModel(ZenithBaseModel):
#     what: str
#     the: str
#     heck: str

# class BarRecord(ZenithBaseRecord, serializer='json_foos'):
#     this: BarModel