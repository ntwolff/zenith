# app/fake_data_producer.py
import faust
from faker import Faker
from datetime import datetime
from .events.models import RegistrationEvent, LoginEvent, Device, IpAddress, Person, Address

#TODO - Allow for a limit to be set on the number of fake records to generate before exiting

app = faust.App('fake-data-producer', broker='kafka://kafka:9092')
fake = Faker()

# Kafka Topics
customer_registration_topic = app.topic('customer_registration', value_type=RegistrationEvent)
login_topic = app.topic('login', value_type=LoginEvent)

@app.timer(interval=1.0)
async def produce_fake_customer_registration_event():
    fake_event = RegistrationEvent(
        event_id=str(fake.uuid4()),
        event_type="registration",
        customer_id=str(fake.uuid4()),
        timestamp=datetime.now(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        person=Person(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=95),
            ssn=fake.ssn(),
            address=Address(
                address_id=str(fake.uuid4()),
                street_address=fake.street_address(),
                city=fake.city(),
                state=fake.state(),
                zip_code=fake.zipcode()
            )
        ),
        device=Device(
            device_id=str(fake.uuid4()),
            user_agent=fake.user_agent()
        ),
        ip_address=IpAddress(
            ip=fake.ipv4()
        )
    )
    await customer_registration_topic.send(value=fake_event)
    print(f"Produced fake customer registration event: {fake_event}")

@app.timer(interval=2.0)
async def produce_fake_login_event():
    fake_event = LoginEvent(
        event_id=str(fake.uuid4()),
        event_type="login",
        customer_id=str(fake.uuid4()),
        timestamp=datetime.now(),
        device=Device(
            device_id=str(fake.uuid4()),
            user_agent=fake.user_agent()
        ),
        ip_address=IpAddress(
            ip=fake.ipv4()
        )
    )
    await login_topic.send(value=fake_event)
    print(f"Produced fake login event: {fake_event}")