from app.config.settings import settings
from app.stream.faust_app import app
from app.stream.topic import event_topic
from app.models.v2 import Event, CustomerEventType, ApplicationEventType, Customer, Device, Address, Application, EmploymentType, SourceType, IpAddress
from faker import Faker
import random
import asyncio

# Initialize Faker
fake = Faker()

# Dictionary to store customer states and reusable values
customer_states = {}
used_ips, used_devices, used_addresses, used_phones, used_emails = [], [], [], [], []


@app.timer(1.0)
async def produce_fake_events() -> None:
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
    await topic.send(value=event)
    
    print(f"Produced {event.__class__.__name__} {event.type}: {event.uid}")


async def generate_fake_customer_registration() -> Event:
    """Generate a fake customer registration event."""
    address = get_or_create_value(used_addresses, lambda: Address(
        uid=str(fake.uuid4()),
        street=fake.street_address(),
        city=fake.city(),
        state=fake.state_abbr(),
        zip=fake.zipcode(),
    ))

    customer = Customer(
        uid=str(fake.uuid4()),
        email=get_or_create_value(used_emails, fake.email),
        phone=get_or_create_value(used_phones, fake.phone_number),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=80),
        ssn=fake.ssn(),
        address=address,
    )

    device = get_or_create_value(used_devices, lambda: Device(
        uid=str(fake.uuid4()),
        device_id=str(fake.uuid4()),
        user_agent=fake.user_agent(),
    ))

    ip_address = get_or_create_value(used_ips, lambda: IpAddress(
        uid=str(fake.uuid4()),
        ipv4=fake.ipv4(),
    ))

    return Event(
        uid=str(fake.uuid4()),
        type=CustomerEventType.CUSTOMER_REGISTRATION.value,
        timestamp=int(asyncio.get_running_loop().time()),
        customer=customer,
        device=device,
        ip_address=ip_address,
    )


async def generate_fake_customer_login(customer_uid: str) -> Event:
    """Generate a fake customer login event."""
    device = get_or_create_value(used_devices, lambda: Device(
        uid=str(fake.uuid4()),
        device_id=str(fake.uuid4()),
        user_agent=fake.user_agent(),
    ))
    ip_address = get_or_create_value(used_ips, lambda: IpAddress(
        uid=str(fake.uuid4()),
        ipv4=fake.ipv4(),
    ))
    return Event(
        uid=str(fake.uuid4()),
        type=CustomerEventType.CUSTOMER_LOGIN.value,
        timestamp=int(asyncio.get_running_loop().time()),
        customer=Customer(uid=customer_uid),
        device=device,
        ip_address=ip_address,
    )


async def generate_fake_application_event(customer_uid: str) -> Event:
    """Generate a fake application event."""
    device = get_or_create_value(used_devices, lambda: Device(
        uid=str(fake.uuid4()),
        device_id=str(fake.uuid4()),
        user_agent=fake.user_agent(),
    ))
    ip_address = get_or_create_value(used_ips, lambda: IpAddress(
        uid=str(fake.uuid4()),
        ipv4=fake.ipv4(),
    ))
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