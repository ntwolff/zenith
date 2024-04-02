"""
Stream Processing Utilities
"""

from app.models.v2 import Event, CustomerEventType, ApplicationEventType
from app.services import RecordService, CustomerService, EventService, AddressService
from app.database.database_interface import GraphDatabaseInterface

class GraphEventProcessor:
    """
    Processor to integrate an event into the graph database.
    """
    def __init__(self, db: GraphDatabaseInterface):
        self.c_service = CustomerService(db)
        self.e_service = EventService(db)
        self.r_service = RecordService(db)
        self.a_service = AddressService(db)

    def process_event(self, event: Event):
        device = event.device
        ip_address = event.ip_address

        #event
        self.e_service.create_record(event)

        #device
        self.r_service.upsert_record(device)
        self.r_service.connect_records(event, device, "HAS")

        #ip_address
        self.r_service.upsert_record(ip_address)
        self.r_service.connect_records(event, ip_address, "HAS")

        if (event.type in CustomerEventType) or (event.type in ApplicationEventType):
            #customer
            customer = event.customer
            self.c_service.upsert_record(customer)
            self.r_service.connect_records(customer, event, "PERFORMS")
            self.r_service.connect_records(customer, device, "USED")
            self.r_service.connect_records(customer, ip_address, "USED")

            ## customer.address
            if customer.address:
                address = self.a_service.validate_address(customer.address)
                self.r_service.upsert_record(address)
                self.r_service.connect_records(customer, address, "RESIDES_AT")

            #pii links
            self.c_service.link_on_pii('email', customer.email)
            self.c_service.link_on_pii('phone', customer.phone)
            self.c_service.link_on_pii('ssn', customer.ssn)

        if event.type in ApplicationEventType:
            #application
            application = event.application
            self.r_service.upsert_record(application)
            self.r_service.connect_records(event, application, "HAS")
            self.r_service.connect_records(customer, application, "OWNS")
            self.r_service.connect_records(application, event, "PERFORMS")
            self.r_service.connect_records(application, device, "USED")
            self.r_service.connect_records(application, ip_address, "USED")
