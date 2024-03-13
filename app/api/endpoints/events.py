from fastapi import APIRouter
from app.models import CustomerEvent, CustomerEventModel
from app.processors import CustomerEventGraphProcessor
from app.api.endpoints import graph_database
import random

router = APIRouter()

@router.post("/customer-event")
def handle_customer_event(event: CustomerEventModel):
    print(f"Received event: {event}")

    faust_event = CustomerEvent.from_model(event)
    processor = CustomerEventGraphProcessor(graph_database)
    processor.process(faust_event)

@router.get("/graph")
def get_graph_data():
    query = """
        MATCH (c:Customer)-[r]->(other)
        RETURN c, other, r
        LIMIT 250
    """
    
    with graph_database.driver.session() as session:
        results = session.run(query)
        nodes = []
        edges = []
        
        # Generate random positions for nodes
        positions = {}
        
        for record in results:
            source_node = record['c']
            target_node = record['other']
            relationship = record['r']
            
            # Generate random positions if not already assigned
            if source_node.id not in positions:
                positions[source_node.id] = (random.uniform(0, 1), random.uniform(0, 1))
            if target_node.id not in positions:
                positions[target_node.id] = (random.uniform(0, 1), random.uniform(0, 1))
            
            source_node_data = {
                'data': {
                    'id': source_node.id,
                    'label': list(source_node.labels)[0],
                    'properties': {**dict(source_node)}
                },
                'x': positions[source_node.id][0],
                'y': positions[source_node.id][1]
            }
            target_node_data = {
                'data': {
                    'id': target_node.id,
                    'label': list(target_node.labels)[0],
                    'properties': {**dict(target_node)}
                },
                'x': positions[target_node.id][0],
                'y': positions[target_node.id][1]
            }
            edge_data = {
                'data': {
                    'source': source_node.id,
                    'target': target_node.id,
                    'type': type(relationship).__name__,
                    'properties': {**dict(relationship)}
                },
                'x1': positions[source_node.id][0],
                'y1': positions[source_node.id][1],
                'x2': positions[target_node.id][0],
                'y2': positions[target_node.id][1]
            }
            
            if source_node_data not in nodes:
                nodes.append(source_node_data)
            if target_node_data not in nodes:
                nodes.append(target_node_data)
            if edge_data not in edges:
                edges.append(edge_data)
        
        return {'elements': {'nodes': nodes, 'edges': edges}}