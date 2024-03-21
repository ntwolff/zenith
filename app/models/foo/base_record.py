import faust
from typing import Any, Type
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from app.models.foo.base_model import ZenithBaseModel

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