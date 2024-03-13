from app.services.customer_service import CustomerService
from app.services.ip_address_service import IpAddressService

class HighVelocityEventProcessor:
    def __init__(self, app, graph_database):
        self.app = app
        self.customer_service = CustomerService(graph_database)
        self.ip_address_service = IpAddressService(graph_database)

    async def process_high_velocity_event(self, stream):
        async for event in stream:
            if event.type == "login_velocity":
                print(f"Processing {event.id} as high velocity login")
                self.customer_service.mark_as_risky(customer_id=event.id, reason="High Velocity Logins")
            
            elif event.type == "ip_velocity":
                print(f"Processing {event.id} as high velocity ip usage")
                self.ip_address_service.mark_as_risky(ip_address_id=event.id, reason="High Velocity IP")
            
            else:
                print(f"Unknown event type: {event.type}")