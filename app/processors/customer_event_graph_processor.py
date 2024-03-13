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
        self.customer_service.create_relationship(customer, "event_id", event.event_id, "PERFORMS")

        #device
        self.device_service.upsert(device)
        self.event_service.create_relationship(event, "device_id", device.device_id, "HAS")
        self.customer_service.create_relationship(customer, "device_id", device.device_id, "USED")

        #ip_address
        self.ip_address_service.upsert(ip_address)
        self.event_service.create_relationship(event, "ip_address_id", ip_address.ip_address_id, "HAS")
        self.customer_service.create_relationship(customer, "ip_address_id", ip_address.ip_address_id, "USED")

        #address
        if customer.address:
            address = self.address_service.validate_address(customer.address)
            self.address_service.upsert(address)
            self.customer_service.create_relationship(customer, "address_id", address.address_id, "RESIDES_AT")

        self.customer_service.link_customers_by_pii('email', event.customer.email)
        self.customer_service.link_customers_by_pii('phone', event.customer.phone)
        self.customer_service.link_customers_by_pii('ssn', event.customer.ssn)
        self.customer_service.link_customers_by_address(event.customer.address)
        
        print(f"Processed event: {event.event_id}")