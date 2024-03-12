# This file produces fake customer registration events on a loop and streams them to the Kafka topic customer_event.

import faust
from faker import Faker
import random
from datetime import datetime
from .models import CustomerEvent, Customer, Device, IpAddress, Address

app = faust.App('fake-producer', broker='kafka://kafka:9092')
fake = Faker()

# Kafka Topics
customer_registration_topic = app.topic('customer_event', value_type=CustomerEvent)

used_ips = []
used_devices = []

@app.timer(interval=2.0)
async def produce_fake_customer_event():
    if (len(used_ips) > 0) & (random.random() < 0.2):
        ip_address_id = random.choice(used_ips)
    else:
        ip_address_id = str(fake.ipv4())
        used_ips.append(ip_address_id)
        
    if (len(used_devices) > 0) & (random.random() < 0.2):
        device_id = random.choice(used_devices)
    else:
        device_id = str(fake.uuid4())
        used_devices.append(device_id)

    fake_event = CustomerEvent(
        id=str(fake.uuid4()),
        type=fake.random_element(elements=("registration", "login")),
        timestamp=datetime.now(),
        customer=Customer(
            id=str(fake.uuid4()),
            email=fake.email(),
            phone=fake.phone_number(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=95),
            ssn=fake.ssn(),
            address=Address(
                id=str(fake.uuid4()),
                street=fake.street_address(),
                city=fake.city(),
                state=fake.state(),
                zip=fake.zipcode()
            ),
        ),
        device=Device(
            id=device_id,
            user_agent=fake.user_agent()
        ),
        ip_address=IpAddress(
            id=ip_address_id,
            ipv4=ip_address_id
        )
    )
    await customer_registration_topic.send(value=fake_event)
    print(f"Produced fake customer registration event: {fake_event}")