from app.models.event import CustomerEvent
from app.services import RecordService, CustomerService, EventService, AddressService
from app.database.database_interface import DatabaseInterface
import logging

class GraphProcessor:
    def __init__(self, db: DatabaseInterface):
        self.c_service = CustomerService(db)
        self.e_service = EventService(db)
        self.r_service = RecordService(db)
        self.a_service = AddressService(db)

    def process(self, event: CustomerEvent):
        customer = event.customer
        device = event.device
        ip_address = event.ip_address

        #event
        self.e_service.create_record(event)
        
        #customer
        customer.last_active_at = event.timestamp
        self.c_service.upsert_record(customer)
        self.r_service.connect_records(customer, event, "PERFORMS")

        #device
        self.r_service.upsert_record(device)
        self.r_service.connect_records(event, device, "HAS")
        self.r_service.connect_records(customer, device, "USED")

        #ip_address
        self.r_service.upsert_record(ip_address)
        self.r_service.connect_records(event, ip_address, "HAS")
        self.r_service.connect_records(customer, ip_address, "USED")

        #address
        if customer.address:
            address = self.a_service.validate_address(customer.address)
            self.r_service.upsert_record(address)
            self.r_service.connect_records(customer, address, "RESIDES_AT")

        #pii links
        self.c_service.link_on_pii('email', event.customer.email)
        self.c_service.link_on_pii('phone', event.customer.phone)
        self.c_service.link_on_pii('ssn', event.customer.ssn)
        
        logging.info(f"Processed event: {event.event_id}")
