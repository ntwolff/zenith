from app.processors.base import BaseProcessor
from app.models.event import CustomerEvent
from app.services import CustomerService, DeviceService, IpAddressService, EventService, AddressService
from app.database.database_interface import DatabaseInterface

class CustomerEventGraphProcessor(BaseProcessor):
    def __init__(self, db: DatabaseInterface):
        super().__init__(db)
        self.customer_service = CustomerService(self.db)
        self.device_service = DeviceService(self.db)
        self.ip_address_service = IpAddressService(self.db)
        self.event_service = EventService(self.db)
        self.address_service = AddressService(self.db)
        
    def process(self, event: CustomerEvent):

        customer = event.customer
        device = event.device
        ip_address = event.ip_address

        #derived properties
        customer.last_active_at = event.timestamp

        #event and customer
        self.event_service.create(event)
        self.customer_service.upsert(customer)
        self.customer_service.create_relationship(customer, event, "PERFORMS")

        #device
        self.device_service.upsert(device)
        self.event_service.create_relationship(event, device, "HAS")
        self.customer_service.create_relationship(customer, device, "USED")

        #ip_address
        self.ip_address_service.upsert(ip_address)
        self.event_service.create_relationship(event, ip_address, "HAS")
        self.customer_service.create_relationship(customer, ip_address, "USED")

        #address
        if customer.address:
            address = customer.address
            self.address_service.upsert(address)
            self.customer_service.create_relationship(customer, address, "RESIDES_AT")
        
        print(f"Processed event: {event.id}")