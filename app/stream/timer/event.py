from app.config.settings import settings
from app.stream.faust_app import app
from app.stream.topic import customer_event_topic, application_event_topic
from app.models import CustomerEvent, ApplicationEvent, CustomerEventTypeEnum, ApplicationEventTypeEnum, Customer, Device, Address
from app.models.application import Application, EmploymentStatusEnum, SourceEnum
from app.models.ip_address import IpAddress
from faker import Faker
import random
import asyncio
import logging

# Initialize Faker
fake = Faker()

# Dictionary to store customer states and reusable values
customer_states = {}
used_ips, used_devices, used_addresses, used_phones, used_emails = [], [], [], [], []

@app.timer(2.0)
async def produce_fake_events() -> None:
    """Produce fake customer and application events."""
    if not settings.fake_data_generation_enabled:
        return

    # Randomly decide whether to create a new customer or use an existing one
    if random.random() < 0.2 or not customer_states:
        # Create a new customer
        customer_event = await generate_fake_customer_registration()
        await send_event(customer_event_topic, customer_event)
        customer_states[customer_event.customer.uid] = CustomerEventTypeEnum.REGISTRATION
    else:
        # Use an existing customer
        customer_id = random.choice(list(customer_states.keys()))
        customer_state = customer_states[customer_id]

        if customer_state == CustomerEventTypeEnum.REGISTRATION:
            # Simulate customer login event
            customer_event = await generate_fake_customer_login(customer_id)
            await send_event(customer_event_topic, customer_event)
            customer_states[customer_id] = CustomerEventTypeEnum.LOGIN
        elif customer_state == CustomerEventTypeEnum.LOGIN:
            # Randomly decide whether to create a login event or an application event
            event_type = random.choice([CustomerEventTypeEnum.LOGIN, ApplicationEventTypeEnum.SUBMISSION])
            if event_type == CustomerEventTypeEnum.LOGIN:
                # Randomly decide whether to create a login event
                if random.random() < 0.3:
                    customer_event = await generate_fake_customer_login(customer_id)
                    await send_event(customer_event_topic, customer_event)
            else:
                # Randomly decide whether to create an application event
                if random.random() < 0.3:
                    application_event = await generate_fake_application_event(customer_id)
                    await send_event(application_event_topic, application_event)

async def send_event(topic, event):
    await topic.send(value=event)
    logging.info(f"Produced {event.__class__.__name__} {event.type}: {event.uid}")

async def generate_fake_customer_registration() -> CustomerEvent:
    """Generate a fake customer registration event."""
    event_id = str(fake.uuid4())
    customer_id = str(fake.uuid4())
    address_id = str(fake.uuid4())
    address = get_or_create_value(used_addresses, lambda: Address(
        uid=address_id,
        address_id=address_id,
        street=fake.street_address(),
        city=fake.city(),
        state=fake.state_abbr(),
        zip=fake.zipcode(),
    ))
    customer = Customer(
        uid=customer_id,
        customer_id=customer_id,
        email=get_or_create_value(used_emails, fake.email),
        phone=get_or_create_value(used_phones, fake.phone_number),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=80),
        ssn=fake.ssn(),
        address=address,
    )
    device_id = str(fake.uuid4())
    device = get_or_create_value(used_devices, lambda: Device(
        uid=device_id,
        device_id=device_id,
        user_agent=fake.user_agent(),
    ))
    ip_address_id = str(fake.uuid4())
    ip_address = get_or_create_value(used_ips, lambda: IpAddress(
        uid=ip_address_id,
        ip_address_id=ip_address_id,
        ipv4=fake.ipv4(),
    ))
    return CustomerEvent(
        uid=event_id,
        event_id=event_id,
        type=CustomerEventTypeEnum.REGISTRATION.value,
        timestamp=int(asyncio.get_running_loop().time()),
        customer=customer,
        device=device,
        ip_address=ip_address,
    )

async def generate_fake_customer_login(customer_id: str) -> CustomerEvent:
    """Generate a fake customer login event."""
    event_id = str(fake.uuid4())
    device_id = str(fake.uuid4())
    device = get_or_create_value(used_devices, lambda: Device(
        uid=device_id,
        device_id=device_id,
        user_agent=fake.user_agent(),
    ))
    ip_address_id = str(fake.uuid4())
    ip_address = get_or_create_value(used_ips, lambda: IpAddress(
        uid=ip_address_id,
        ip_address_id=ip_address_id,
        ipv4=fake.ipv4(),
    ))
    return CustomerEvent(
        uid=event_id,
        event_id=event_id,
        type=CustomerEventTypeEnum.LOGIN.value,
        timestamp=int(asyncio.get_running_loop().time()),
        customer=Customer(uid=customer_id, customer_id=customer_id),
        device=device,
        ip_address=ip_address,
    )

async def generate_fake_application_event(customer_id: str) -> ApplicationEvent:
    """Generate a fake application event."""
    event_id = str(fake.uuid4())
    device_id = str(fake.uuid4())
    device = get_or_create_value(used_devices, lambda: Device(
        uid=device_id,
        device_id=device_id,
        user_agent=fake.user_agent(),
    ))
    ip_address_id = str(fake.uuid4())
    ip_address = get_or_create_value(used_ips, lambda: IpAddress(
        uid=ip_address_id,
        ip_address_id=ip_address_id,
        ipv4=fake.ipv4(),
    ))
    application_id = str(fake.uuid4())
    return ApplicationEvent(
        uid=event_id,
        event_id=event_id,
        type=ApplicationEventTypeEnum.SUBMISSION.value,
        timestamp=int(asyncio.get_running_loop().time()),
        customer=Customer(uid=customer_id, customer_id=customer_id),
        application=Application(
            uid=application_id,
            application_id=application_id,
            source=fake.random_element(list(SourceEnum)),
            income=fake.random_int(min=10000, max=200000),
            employment_status=fake.random_element(list(EmploymentStatusEnum)),
        ),
        device=device,
        ip_address=ip_address,
    )

def get_or_create_value(collection, create_func):
    if collection and random.random() < 0.2:
        return random.choice(collection)
    else:
        value = create_func() if callable(create_func) else create_func
        collection.append(value)
        return value