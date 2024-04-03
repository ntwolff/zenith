import pydantic
from app.database.base import BaseDatabase

class GraphService:
    def __init__(self, database: BaseDatabase):
        self.db = database

    def create(self, label: str, properties: dict):
        properties_str = ', '.join([f'{k}:"{v}"' for k, v in properties.items()])
        query = """
            CREATE (n:{label} {{{properties_str}}})
        """.format(label=label, properties_str=properties_str)
        self.db.execute_query(query)


    def upsert(self, label: str, id_key: str, id_val: str, properties: dict):
        properties_str = ', '.join([f'{k}:"{v}"' for k, v in properties.items()])
        query = """
            MERGE (n:{label} {{{id_key}: "{id_val}"}})
            ON CREATE SET n += {{{properties_str}}}
            ON MATCH SET n += {{{properties_str}}}
        """.format(label=label, id_key=id_key, id_val=id_val, properties_str=properties_str)
        self.db.execute_query(query)


    def upsert_record(self, record: pydantic.BaseModel):
        self.upsert(record.__class__.__name__, "uid", record.uid, record.dict())


    def connect(self,
            from_label:str, from_id_key:str, from_id_val:str,
            to_label: str, to_id_key: str, to_id_val: str,
            rel_type: str):
        query = """
            MATCH (f:{from_label} {{{from_id_key}: "{from_id_val}"}})
            MATCH (t:{to_label} {{{to_id_key}: "{to_id_val}"}})
            MERGE (f)-[r:{rel_type}]->(t)
        """.format(
            from_label=from_label, from_id_key=from_id_key, from_id_val=from_id_val,
            to_label=to_label, to_id_key=to_id_key, to_id_val=to_id_val,
            rel_type=rel_type)
        self.db.execute_query(query)


    def connect_records(self,
                        from_model: pydantic.BaseModel,
                        to_model: pydantic.BaseModel,
                        rel_type: str):
        self.connect(
            from_model.__class__.__name__, "uid", from_model.uid,
            to_model.__class__.__name__, "uid", to_model.uid,
            rel_type)
