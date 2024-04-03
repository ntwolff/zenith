from app.models import Event, CustomerEventType, ApplicationEventType
from app.services import GraphService, CustomerService, EventService
from app.services.external import GoogleMapsService, IpInfoService
from app.database.base import BaseDatabase

class GraphEventProcessor:
    def __init__(self, db: BaseDatabase):
        self.g_service = GraphService(db)
        self.c_service = CustomerService(db)
        self.e_service = EventService(db)
        self.gmaps_service = GoogleMapsService()
        self.ip_info_service = IpInfoService()

    def process_event(self, event: Event):
        device = event.device
        ip_address = event.ip_address
        assert device and ip_address, "Missing required event fields"

        #event
        self.e_service.create_record(event)

        #device
        self.g_service.upsert_record(device)
        self.g_service.connect_records(event, device, "HAS")

        #ip_address
        ip_info = self.ip_info_service.enrich(event.ip_address) #external service enrich
        self.g_service.upsert_record(ip_address)
        self.g_service.connect_records(event, ip_address, "HAS")

        if (event.event_type in CustomerEventType) or (event.event_type in ApplicationEventType):
            #customer
            customer = event.customer
            self.c_service.upsert_record(customer)
            self.g_service.connect_records(customer, event, "PERFORMS")
            self.g_service.connect_records(customer, device, "USED")
            self.g_service.connect_records(customer, ip_address, "USED")

            ## customer.address
            if customer.address:
                address_info = self.gmaps_service.enrich(event.customer.address) #external service enrich
                self.g_service.upsert_record(customer.address)
                self.g_service.connect_records(customer, customer.address, "RESIDES_AT")

            #pii links
            self.c_service.link_on_pii('email', customer.email)
            self.c_service.link_on_pii('phone', customer.phone)
            self.c_service.link_on_pii('ssn', customer.ssn)

        if event.event_type in ApplicationEventType:
            #application
            application = event.application
            self.g_service.upsert_record(application)
            self.g_service.connect_records(event, application, "HAS")
            self.g_service.connect_records(customer, application, "OWNS")
            self.g_service.connect_records(application, event, "PERFORMS")
            self.g_service.connect_records(application, device, "USED")
            self.g_service.connect_records(application, ip_address, "USED")
