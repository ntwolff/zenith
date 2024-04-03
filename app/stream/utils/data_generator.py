import random
from faker import Faker
from app.models.customer import Customer, Address
from app.models.event import Device, IpAddress

class FakeData:
    def __init__(self, fake: Faker):
        self.fake = fake
        self.used_ips = []
        self.used_devices = []
        self.used_addresses = []
        self.used_phones = []
        self.used_emails = []

    def get_or_create_value(self, collection, create_func):
        if collection and random.random() < 0.2:
            return random.choice(collection)
        else:
            value = create_func() if callable(create_func) else create_func
            collection.append(value)
            return value

    def get_or_create_device(self) -> Device:
        return self.get_or_create_value(self.used_devices, lambda: Device(
            uid=str(self.fake.uuid4()),
            device_id=str(self.fake.uuid4()),
            user_agent=self.fake.user_agent(),
        ))

    def get_or_create_ip_address(self) -> IpAddress:
        return self.get_or_create_value(self.used_ips, lambda: IpAddress(
            uid=str(self.fake.uuid4()),
            ipv4=self.fake.ipv4(),
        ))

    def get_or_create_email(self) -> str:
        return self.get_or_create_value(self.used_emails, self.fake.email)

    def get_or_create_phone(self) -> str:
        return self.get_or_create_value(self.used_phones, self.fake.phone_number)

    def get_or_create_address(self) -> Address:
        return self.get_or_create_value(self.used_addresses, lambda: Address(
            uid=str(self.fake.uuid4()),
            street=self.fake.street_address(),
            city=self.fake.city(),
            state=self.fake.state_abbr(),
            zip=self.fake.zipcode(),
        ))

    def create_customer(self) -> Customer:
        return Customer(
            uid=str(self.fake.uuid4()),
            email=self.get_or_create_email(),
            phone=self.get_or_create_phone(),
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            date_of_birth=self.fake.date_of_birth(minimum_age=18, maximum_age=80),
            ssn=self.fake.ssn(),
            address=self.get_or_create_address(),
        )