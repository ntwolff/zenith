"""
Customer Service
"""

from datetime import datetime
from app.models import Customer
from ._base import BaseService

class CustomerService(BaseService):
    def upsert_record(self, record: Customer):
        properties = record.dict()
        properties.pop("address")
        label = record.__class__.__name__
        super().upsert(label, "uid", record.uid, properties)

    def mark_as_risky(self, uid: str, reason: str):
        properties = {
            "risky": True,
            "risky_since": datetime.now(),
            "risky_reason": reason
        }
        label = "Customer"

        super().upsert(label, "uid", uid, properties)

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
