from app.models.v2 import Customer
from .base_service import BaseService
from datetime import datetime

class CustomerService(BaseService):
    def upsert_record(self, customer: Customer):
        properties = customer.dict()
        properties.pop("address")
        label = customer.__class__.__name__
        super().upsert(label, "uid", customer.uid, properties)

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