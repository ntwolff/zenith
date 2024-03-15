from app.config.settings import settings
from app.faust.app import faust_app
from app.faust.topic.customer_event import customer_event_topic
from app.faust.topic.application_event import application_event_topic
from faker import Faker
from datetime import datetime
from app.models import Customer, Device, Address
from app.models.event import Event, CustomerEvent, ApplicationEvent
from app.models.application import Application, SourceEnum, EmploymentStatusEnum
from app.models.ip_address import IpAddress
import random
import logging

fake = Faker('en_US')
used_customer_ids, used_ips, used_devices, used_phones, used_addresses = [], [], [], [], []

@faust_app.timer(2.0)
async def produce_fake_customer_events():
    if not settings.fake_data_generation_enabled:
        return

    customer_event = await generate_customer_event()
    await customer_event_topic.send(value=customer_event)
    
    application_event = await generate_application_event(customer_event)
    await application_event_topic.send(value=application_event)

async def generate_customer_event() -> CustomerEvent:
    customer_id = get_or_create_value(used_customer_ids, lambda: str(fake.uuid4()))
    event_type = "login" if customer_id in used_customer_ids else "registration"

    ip_address_id = get_or_create_value(used_ips, lambda: str(fake.ipv4()))
    device_id = get_or_create_value(used_devices, lambda: str(fake.uuid4()))
    phone = get_or_create_value(used_phones, fake.phone_number)
    event_id = str(fake.uuid4())
    address = get_or_create_value(used_addresses, lambda: Address(
        uid=str(fake.uuid4()),
        address_id=str(fake.uuid4()),
        street=fake.street_address(),
        city=fake.city(),
        state=fake.state(),
        zip=fake.zipcode(),
        is_valid=True,
        latitude=fake.latitude(),
        longitude=fake.longitude(),
    ))

    if random.random() < 0.05:
        isFraud = True
    else:
        isFraud = False

    fake_customer_event = CustomerEvent(
        uid=event_id,
        event_id=event_id,
        type=event_type,
        timestamp=int(datetime.now().timestamp()),
        customer=Customer(
            uid=customer_id,
            customer_id=customer_id,
            email=fake.email(),
            phone=phone,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=98),
            ssn=fake.ssn(),
            address=address,
            is_fraud=isFraud
        ),
        device=Device(
            uid=device_id,
            device_id=device_id,
            user_agent=fake.user_agent()
        ),
        ip_address=IpAddress(
            uid=ip_address_id,
            ip_address_id=ip_address_id,
            ipv4=ip_address_id
        )
    )
    logging.info(f"Added CustomerEvent: {fake_customer_event.uid}")
    return fake_customer_event

async def generate_application_event(customer_event: CustomerEvent) -> ApplicationEvent:
    event_id = str(fake.uuid4())
    
    fake_app_event = ApplicationEvent(
        uid=event_id,
        event_id=event_id,
        type="submission",
        timestamp=int(datetime.now().timestamp()),
        customer=customer_event.customer,
        application=Application(
            uid=str(fake.uuid4()),
            application_id=str(fake.uuid4()),
            source=random.choice(list(SourceEnum)).value,
            income=random.uniform(10000, 200000),
            employment_status=random.choice(list(EmploymentStatusEnum)).value
        ),
        device=customer_event.device,
        ip_address=customer_event.ip_address
    )
    logging.info(f"Added ApplicationEvent: {fake_app_event.uid}")
    return fake_app_event

def get_or_create_value(collection, create_func, reuse_probability=0.2):
    if collection and random.random() < reuse_probability:
        return random.choice(collection)
    else:
        value = create_func()
        collection.append(value)
        return value