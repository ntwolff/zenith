import faust
from faker import Faker
import random
from datetime import datetime
from .models import CustomerEvent, Customer, Device, IpAddress, Address
from app.config.settings import settings

app = faust.App('fake-producer', broker='kafka://kafka:9092')
fake = Faker('en_US')

# Kafka Topics
customer_registration_topic = app.topic('customer_event', value_type=CustomerEvent)

used_customer_ids = []
used_ips = []
used_devices = []
used_phones = []
used_addresses = []

@app.timer(interval=1.0)
async def produce_fake_customer_event():
    if not settings.fake_data_generation_enabled:
        return

    #customer id
    if (len(used_customer_ids) > 0) & (random.random() < 0.2):
        customer_id = random.choice(used_customer_ids)
        event_type = "login"
    else:
        customer_id = str(fake.uuid4())
        event_type = "registration"
        used_customer_ids.append(customer_id)
    
    #ip address
    if (len(used_ips) > 0) & (random.random() < 0.2):
        ip_address_id = random.choice(used_ips)
    else:
        ip_address_id = str(fake.ipv4())
        used_ips.append(ip_address_id)
    
    #device id
    if (len(used_devices) > 0) & (random.random() < 0.2):
        device_id = random.choice(used_devices)
    else:
        device_id = str(fake.uuid4())
        used_devices.append(device_id)

    #phones
    if (len(used_phones) > 0) & (random.random() < 0.1):
        phone = random.choice(used_phones)
    else:
        phone = fake.phone_number()
        used_phones.append(phone)

    #addresses
    if (len(used_addresses) > 0) & (random.random() < 0.1):
        address = random.choice(used_addresses)
    else:
        address = Address(
                address_id=str(fake.uuid4()),
                street=fake.street_address(),
                city=fake.city(),
                state=fake.state(),
                zip=fake.zipcode(),
                is_valid=True,
                latitude=fake.latitude(),
                longitude=fake.longitude(),
                )
        used_addresses.append(address)

    fake_event = CustomerEvent(
        event_id=str(fake.uuid4()),
        type=event_type,
        timestamp=int(datetime.now().timestamp()),
        customer=Customer(
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
            device_id=device_id,
            user_agent=fake.user_agent()
        ),
        ip_address=IpAddress(
            ip_address_id=ip_address_id,
            ipv4=ip_address_id
        )
    )
    await customer_registration_topic.send(value=fake_event)
    print(f"Produced fake customer registration event: {fake_event}")