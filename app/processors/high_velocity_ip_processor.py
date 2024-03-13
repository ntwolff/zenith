from app.models import CustomerEvent, HighVelocityEvent

class HighVelocityIpProcessor:
    def __init__(self, app, window_size, window_expires):
        self.app = app
        self.ip_velocity_table = app.Table('ip_velocity', default=int).tumbling(
            size=window_size,
            expires=window_expires,
        )
        self.high_velocity_topic = app.topic('high_velocity_event', value_type=dict)

    async def detect_high_velocity_ip_usage(self, stream):
        async for event in stream.group_by(CustomerEvent.ip_address.ip_address_id):
            self.ip_velocity_table[event.ip_address.ip_address_id] += 1
            if self.ip_velocity_table[event.ip_address.ip_address_id].now() > 1:
                print(f"Detected {self.ip_velocity_table[event.ip_address.ip_address_id].now()} in the past 5 minutes for ip address: {event.ip_address.ip_address_id}")

                payload = HighVelocityEvent(
                    type="ip_velocity",
                    id=event.ip_address.ip_address_id,
                    event_id=event.event_id,
                    event_type=event.type
                )
                await self.high_velocity_topic.send(value=payload)

                # Results Cypher Query
                # ------------------------------------------------
                # MATCH (i:IpAddress {risky: True})<-[:USED]-(c:Customer)
                # MATCH (c)-[:PERFORMS]->(e:Event)-[:HAS]->(i)
                # RETURN i, c, count(e)
                # RETURN i.ipv4, c.id, c.first_name, c.last_name, c.email, count(e)