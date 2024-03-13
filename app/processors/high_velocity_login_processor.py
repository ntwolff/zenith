from app.models import CustomerEvent, HighVelocityEvent

class HighVelocityLoginProcessor:
    def __init__(self, app, window_size, window_expires):
        self.app = app
        self.login_velocity_table = app.Table('login_velocity', default=int).tumbling(
            size=window_size,
            expires=window_expires,
        )
        self.high_velocity_topic = app.topic('high_velocity_event', value_type=dict)

    async def detect_high_velocity_customer_login(self, stream):
        async for event in stream.filter(lambda e: e.type == "login").group_by(CustomerEvent.customer.id):
            self.login_velocity_table[event.customer.id] += 1
            if self.login_velocity_table[event.customer.id].now() > 1:
                print(f"Detected {self.login_velocity_table[event.customer.id].now()} logins in the past 5 minutes for customer id: {event.customer.id}")
                
                payload = HighVelocityEvent(
                    type="login_velocity",
                    id=event.customer.id,
                    event_id=event.id,
                    event_type=event.type
                )
                await self.high_velocity_topic.send(value=payload)