import random
import asyncio
from faker import Faker
from app.config.settings import settings
from app.stream.faust_app import app
from app.stream.topics import event_topic
from app.stream.utils.loggers import timer_logger
from app.stream.utils.event_generator import FakeEvent

# Initialize the Fakers
fake = Faker()
event_generator = FakeEvent(fake)

@app.timer(1.0)  # 1s Interval
async def spawn_event_data() -> None:
    """Produce fake customer and application events."""
    if not settings.fake_data_generation_enabled:
        return

    # Randomly decide whether to create a new customer or use an existing one
    if random.random() < 0.2 or not event_generator.customer_states:
        # Create a new customer
        customer_event = await event_generator.generate_customer_registration_event()
        await send_event(event_topic, customer_event)
    else:
        # Use an existing customer
        await event_generator.generate_customer_event()

async def send_event(topic, event):
    """Send an event to the specified topic."""
    await topic.send(value=event)
    timer_logger("generate_synthetic_data", topic, event)