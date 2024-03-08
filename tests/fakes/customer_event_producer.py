import faust
from app.models import Address, Device, IpAddress, CustomerRegisteredEvent
from faker import Faker

fake = Faker()

# ------------------------
# Fake Faust Producer
# CustomerEvents
# ------------------------

# If you run the producer and consumer on the same port, you will get an error, please use different ports. Ex:
# python consumer.py worker -p 6067 // python producer.py worker -p 6068
# TODO - automatically resolve port contention

## Setup

app = faust.App('fake-zenith', broker='kafka://localhost:9092')

if app.conf.env == 'production':
    raise Exception('This script should not be run in a production environment')

## CustomerRegisteredEvent

customer_registered_topic = app.topic('event__customer_registration', value_type=CustomerRegisteredEvent)

@app.timer(interval=1.0)
async def produce_fake_data():
    fake_customer = CustomerRegisteredEvent(
        customer_id=fake.uuid4(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        name=fake.name(),
        date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d'),
        ssn=fake.ssn(),
        address=Address(
            street=fake.street_address(),
            city=fake.city(),
            state=fake.state(),
            zip_code=fake.zipcode(),
            country='US'
        ),
        device=Device(
            device_id=fake.uuid4(),
            user_agent=fake.user_agent()
        ),
        ip_address=IpAddress(
            ip=fake.ipv4()
        ),
        timestamp=fake.unix_time()
    )
    await customer_registered_topic.send(value=fake_customer)