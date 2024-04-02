"""
Synthentic Data Generation

***

Features:
- Fake event data
- Random re-use of data
- Sends to Event topic

@TODO: 
- Move data generation to a util class
"""

import random
import asyncio
from faker import Faker
from app.config.settings import settings
from app.stream.faust_app import app
from app.stream.topic import event_topic
from app.models.v2.event import Event, CustomerEventType, ApplicationEventType
from app.models.v2.customer import Customer
from app.models.v2.user import Device, IpAddress
from app.models.v2.address import Address
from app.models.v2.application import Application, EmploymentType, SourceType
from app.stream.util.loggers import timer_logger

# Initialize Faker
fake = Faker()


# Dictionary to store customer states and reusable values
customer_states = {}
used_ips, used_devices, used_addresses, used_phones, used_emails = [], [], [], [], []


# Faust timer running on a static interval (in seconds)
@app.timer(1.0)
async def generate_synthetic_data() -> None:
    """Produce fake customer and application events."""
    if not settings.fake_data_generation_enabled:
        return

    # Randomly decide whether to create a new customer or use an existing one
    if random.random() < 0.2 or not customer_states:
        # Create a new customer
        customer_event = await generate_fake_customer_registration()
        await send_event(event_topic, customer_event)
        customer_states[customer_event.customer.uid] = CustomerEventType.CUSTOMER_REGISTRATION
    else:
        # Use an existing customer
        customer_uid = random.choice(list(customer_states.keys()))
        customer_state = customer_states[customer_uid]

        if customer_state == CustomerEventType.CUSTOMER_REGISTRATION:
            # Simulate customer login event
            customer_event = await generate_fake_customer_login(customer_uid)
            await send_event(event_topic, customer_event)
            customer_states[customer_uid] = CustomerEventType.CUSTOMER_LOGIN
        
        elif customer_state == CustomerEventType.CUSTOMER_LOGIN:
            # Randomly decide whether to create a login event or an application event
            event_type = random.choice([CustomerEventType.CUSTOMER_LOGIN, ApplicationEventType.APPLICATION_SUBMISSION])
            
            if event_type == CustomerEventType.CUSTOMER_LOGIN:
                # Randomly decide whether to create a login event
                if random.random() < 0.3:
                    customer_event = await generate_fake_customer_login(customer_uid)
                    await send_event(event_topic, customer_event)
            else:
                # Randomly decide whether to create an application event
                if random.random() < 0.3:
                    application_event = await generate_fake_application_event(customer_uid)
                    await send_event(event_topic, application_event)


async def send_event(topic, event: Event):
    """Send an event to the specified topic."""
    await topic.send(value=event)
    timer_logger("generate_synthetic_data", topic, event)


async def generate_fake_customer_registration() -> Event:
    """Generate a fake customer registration event."""
    return Event(
        uid=str(fake.uuid4()),
        type=CustomerEventType.CUSTOMER_REGISTRATION.value,
        timestamp=int(asyncio.get_running_loop().time()),
        customer=create_customer(),
        device=get_or_create_device(),
        ip_address=get_or_create_ip_address(),
    )


async def generate_fake_customer_login(customer_uid: str) -> Event:
    """Generate a fake customer login event."""
    return Event(
        uid=str(fake.uuid4()),
        type=CustomerEventType.CUSTOMER_LOGIN.value,
        timestamp=int(asyncio.get_running_loop().time()),
        customer=Customer(uid=customer_uid),
        device=get_or_create_device(),
        ip_address=get_or_create_ip_address(),
    )


async def generate_fake_application_event(customer_uid: str) -> Event:
    """Generate a fake application submission event."""
    return Event(
        uid=str(fake.uuid4()),
        type=ApplicationEventType.APPLICATION_SUBMISSION.value,
        timestamp=int(asyncio.get_running_loop().time()),
        customer=Customer(uid=customer_uid),
        application=Application(
            uid=str(fake.uuid4()),
            source=fake.random_element(list(SourceType)),
            income=fake.random_int(min=10000, max=200000),
            employment_status=fake.random_element(list(EmploymentType)),
        ),
        device=get_or_create_device(),
        ip_address=get_or_create_ip_address(),
    )


# Utility functions to get or create reusable values

def get_or_create_value(collection, create_func):
    value = None
    if collection and random.random() < 0.2:
        value = random.choice(collection)
    else:
        value = create_func() if callable(create_func) else create_func
        collection.append(value)
    
    return value


def get_or_create_device():
    return get_or_create_value(used_devices, lambda: Device(
        uid=str(fake.uuid4()),
        device_id=str(fake.uuid4()),
        user_agent=fake.user_agent(),
    ))


def get_or_create_ip_address():
    return get_or_create_value(used_ips, lambda: IpAddress(
        uid=str(fake.uuid4()),
        ipv4=fake.ipv4(),
    ))


def get_or_create_email():
    return get_or_create_value(used_emails, fake.email)


def get_or_create_phone():
    return get_or_create_value(used_phones, fake.phone_number)


def get_or_create_address():
    return get_or_create_value(used_addresses, lambda: Address(
        uid=str(fake.uuid4()),
        street=fake.street_address(),
        city=fake.city(),
        state=fake.state_abbr(),
        zip=fake.zipcode(),
    ))


def create_customer():
    return Customer(
        uid=str(fake.uuid4()),
        email=get_or_create_email(),
        phone=get_or_create_phone(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=80),
        ssn=fake.ssn(),
        address = get_or_create_address()
    )
