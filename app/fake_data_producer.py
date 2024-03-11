# app/fake_data_producer.py
import faust
from faker import Faker
from .events.models import CustomerRegistrationEvent, LoginEvent, Device, IpAddress

app = faust.App('fake-data-producer', broker='kafka://kafka:9092')
fake = Faker()

# Kafka Topics
customer_registration_topic = app.topic('customer_registration', value_type=CustomerRegistrationEvent)
login_topic = app.topic('login', value_type=LoginEvent)

@app.timer(interval=1.0)
async def produce_fake_customer_registration_event():
    fake_event = CustomerRegistrationEvent(
        customer_id=str(fake.uuid4()),
        email=fake.email(),
        phone_number=fake.phone_number(),
        device=Device(
            device_id=str(fake.uuid4()),
            user_agent=fake.user_agent()
        ),
        ip_address=IpAddress(
            ip=fake.ipv4()
        )
        # Add more fake data fields as needed
    )
    await customer_registration_topic.send(value=fake_event)
    print(f"Produced fake customer registration event: {fake_event}")

@app.timer(interval=2.0)
async def produce_fake_login_event():
    fake_event = LoginEvent(
        customer_id=str(fake.uuid4()),
        timestamp=fake.unix_time(),
        device=Device(
            device_id=str(fake.uuid4()),
            user_agent=fake.user_agent()
        ),
        ip_address=IpAddress(
            ip=fake.ipv4()
        )
        # Add more fake data fields as needed
    )
    await login_topic.send(value=fake_event)
    print(f"Produced fake login event: {fake_event}")