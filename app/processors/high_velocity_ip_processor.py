from app.models.event import CustomerEvent
from app.services.ip_address_service import IpAddressService
from datetime import timedelta

class HighVelocityIpProcessor:
    def __init__(self, app, ip_address_service: IpAddressService):
        self.app = app
        self.ip_address_service = ip_address_service
        self.ip_velocity_table = app.Table('ip_velocity', default=int, partitions=8).tumbling(
            size=timedelta(minutes=5),
            expires=timedelta(hours=1),
        )

    async def detect_high_velocity_ip_usage(self, stream):
        async for event in stream.group_by(CustomerEvent.ip_address.id):
            self.ip_velocity_table[event.ip_address.id] += 1
            if self.ip_velocity_table[event.ip_address.id].now() > 1:
                print(f"Detected {self.ip_velocity_table[event.ip_address.id].now()} in the past 5 minutes for ip address: {event.ip_address.id}")
                await self.ip_address_service.mark_as_risky(event.ip_address.id, "High Velocity IP")


    # Results Cypher Query
    # ------------------------------------------------
    # MATCH (i:IpAddress {risky: True})<-[:USED]-(c:Customer)
    # MATCH (c)-[:PERFORMS]->(e:Event)-[:HAS]->(i)
    # RETURN i, c, count(e)
    # RETURN i.ipv4, c.id, c.first_name, c.last_name, c.email, count(e)