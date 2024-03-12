from app.models.event import CustomerEvent
from app.services.customer_service import CustomerService
from datetime import timedelta

class HighVelocityLoginProcessor:
    def __init__(self, app, customer_service: CustomerService):
        self.app = app
        self.customer_service = customer_service
        self.login_velocity_table = app.Table('login_velocity', default=int, partitions=8).tumbling(
            size=timedelta(minutes=5),
            expires=timedelta(hours=1),
        )

    async def detect_high_velocity_customer_login(self, stream):
        async for event in stream.filter(lambda e: e.type == "login").group_by(CustomerEvent.customer.id):
            self.login_velocity_table[event.customer.id] += 1
            if self.login_velocity_table[event.customer.id].now() > 1:
                print(f"Detected {self.login_velocity_table[event.customer.id].now()} logins in the past 5 minutes for customer id: {event.customer.id}")
                await self.customer_service.mark_as_risky(event.customer.id, "High Velocity Logins")