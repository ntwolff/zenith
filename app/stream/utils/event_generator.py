import random
import asyncio
from typing import Dict
from faker import Faker
from app.models.event import Event, CustomerEventType, ApplicationEventType
from app.models.customer import Customer
from app.models.application import Application, EmploymentType, SourceType
from app.stream.utils.data_generator import FakeData
from app.stream.utils.loggers import timer_logger
from app.stream.topics import event_topic

class FakeEvent:
    def __init__(self, fake: Faker):
        self.fake = fake
        self.data_generator = FakeData(fake)
        self.customer_states: Dict[str, CustomerEventType] = {}

    async def generate_customer_registration_event(self) -> Event:
        """Generate a fake customer registration event."""
        customer = self.data_generator.create_customer()
        device = self.data_generator.get_or_create_device()
        ip_address = self.data_generator.get_or_create_ip_address()

        event = Event(
            uid=str(self.fake.uuid4()),
            event_type=CustomerEventType.CUSTOMER_REGISTRATION.value,
            timestamp=int(asyncio.get_running_loop().time()),
            customer=customer,
            device=device,
            ip_address=ip_address,
        )

        self.customer_states[customer.uid] = CustomerEventType.CUSTOMER_REGISTRATION
        return event

    async def generate_customer_event(self) -> None:
        """Generate a customer event based on the customer state."""
        customer_uid = random.choice(list(self.customer_states.keys()))
        customer_state = self.customer_states[customer_uid]

        if customer_state == CustomerEventType.CUSTOMER_REGISTRATION:
            await self.generate_customer_login_event(customer_uid)
        elif customer_state == CustomerEventType.CUSTOMER_LOGIN:
            await self.generate_login_or_application_event(customer_uid)

    async def generate_customer_login_event(self, customer_uid: str) -> None:
        """Generate a fake customer login event."""
        event = Event(
            uid=str(self.fake.uuid4()),
            event_type=CustomerEventType.CUSTOMER_LOGIN.value,
            timestamp=int(asyncio.get_running_loop().time()),
            customer=Customer(uid=customer_uid),
            device=self.data_generator.get_or_create_device(),
            ip_address=self.data_generator.get_or_create_ip_address(),
        )

        self.customer_states[customer_uid] = CustomerEventType.CUSTOMER_LOGIN
        await self.send_event(event)

    async def generate_login_or_application_event(self, customer_uid: str) -> None:
        """Generate a login event or an application event based on random chance."""
        event_type = random.choice([
            CustomerEventType.CUSTOMER_LOGIN,
            ApplicationEventType.APPLICATION_SUBMISSION
        ])

        if event_type == CustomerEventType.CUSTOMER_LOGIN:
            if random.random() < 0.3:
                await self.generate_customer_login_event(customer_uid)
        else:
            if random.random() < 0.3:
                await self.generate_application_event(customer_uid)

    async def generate_application_event(self, customer_uid: str) -> None:
        """Generate a fake application submission event."""
        application = Application(
            uid=str(self.fake.uuid4()),
            source=self.fake.random_element(list(SourceType)),
            income=self.fake.random_int(min=10000, max=200000),
            employment_status=self.fake.random_element(list(EmploymentType)),
        )

        event = Event(
            uid=str(self.fake.uuid4()),
            event_type=ApplicationEventType.APPLICATION_SUBMISSION.value,
            timestamp=int(asyncio.get_running_loop().time()),
            customer=Customer(uid=customer_uid),
            application=application,
            device=self.data_generator.get_or_create_device(),
            ip_address=self.data_generator.get_or_create_ip_address(),
        )

        await self.send_event(event)

    async def send_event(self, event: Event) -> None:
        """Send an event to the event topic."""
        await event_topic.send(value=event)
        timer_logger("generate_synthetic_data", event_topic, event)