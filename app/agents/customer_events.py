from app.main import app, customer_registered_topic, escalation_topic
from app.graph import driver, create_customer_graph
from shared.utilities import FuzzyMatching
from collections import defaultdict
from datetime import datetime, timedelta

fuzzy = FuzzyMatching()

# CUSTOMER EVENT AGENTS

## ------------------------
## CustomerRegistrationEvent
## ------------------------

### GRAPH PROCESSING

@app.agent(customer_registered_topic)
async def process_customer_registration_event(stream):
    async for event in stream:
        with driver.session() as session:
            session.write_transaction(create_customer_graph, event)
        
        # Perform ML predictions and evaluate decisions
        # Enrich the graph and store computations (RocksDB)
            
        print(f'Processed customer registered event for {event.customer_id}')


### VELOCITY CHECKS

state = defaultdict(list)

@app.agent(customer_registered_topic)
async def velocity_check(stream):
    async for event in stream:
        current_timestamp = datetime.fromtimestamp(event.timestamp)
        
        for key in ['ssn', 'email', 'phone_number', 'address']:
            value = getattr(event, key)
            if key == 'address':
                value = fuzzy.hash_address(value)
            if key == 'phone_number':
                value = fuzzy.standardize_phone_number(value)
            if key == 'ssn':
                value = fuzzy.hash_ssn(value)
            if key == 'email':
                value = value.lower()
            
            state[key].append((value, current_timestamp))
            state[key] = [(v, t) for v, t in state[key] if t > current_timestamp - timedelta(days=30)]
            
            if len(state[key]) > 5:
                await escalation_topic.send(value=event)