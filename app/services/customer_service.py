from app.models import Customer
from .base import GraphService

class CustomerService(GraphService):
    def upsert_record(self, record: Customer):
        properties = record.dict()
        properties.pop("address")
        label = record.__class__.__name__
        super().upsert(label, "uid", record.uid, properties)

    def link_on_pii(self, pii_type, pii_value):
        query = """
            MATCH (c1:Customer)
            MATCH (c2:Customer)
            WHERE c1 <> c2
            AND c1[$pii_type] = $pii_value
            AND c2[$pii_type] = $pii_value
            MERGE (c1)-[:SHARES_PII {type: $pii_type, value: $pii_value}]-(c2)
        """
        self.db.execute_query(query, pii_type=pii_type, pii_value=pii_value)
