from app.config.settings import settings
from app.faust.app import faust_app
from app.faust.topic.customer_event import customer_event_topic
from faker import Faker
from datetime import datetime
from app.models import CustomerEvent, Customer, Device, IpAddress, Address
import random
import logging

fake = Faker('en_US')
used_customer_ids, used_ips, used_devices, used_phones, used_addresses = [], [], [], [], []

@faust_app.timer(1.0)
async def produce_fake_customer_events():
    if not settings.fake_data_generation_enabled:
        return

    record = generate_record()
    await customer_event_topic.send(value=record)
    return {"success": True}

def generate_record() -> CustomerEvent:
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

    fake_event = CustomerEvent(
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
    logging.info(f"Added CustomerEvent: {fake_event.uid}")
    return fake_event

def get_or_create_value(collection, create_func, reuse_probability=0.2):
    if collection and random.random() < reuse_probability:
        return random.choice(collection)
    else:
        value = create_func()
        collection.append(value)
        return value