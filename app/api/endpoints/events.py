from fastapi import APIRouter
from app.models import CustomerEvent, Customer, Address, Device, IpAddress, CustomerEventModel
from app.processors import CustomerEventGraphProcessor
from app.api.endpoints import graph_database

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
        RETURN ID(c) as c_id, c, ID(other) as other_id, other, r
        LIMIT 250
    """
    
    with graph_database.driver.session() as session:
        results = session.run(query)
        nodes = []
        edges = []

        print (results)

        for record in results:
            source_node_id = record['c_id']
            source_node = record['c']
            target_node_id = record['other_id']
            target_node = record['other']
            relationship = record['r']

            source_node_data = {
                'data': {
                    'id': source_node_id,
                    'label': list(source_node.labels)[0],
                    **dict(source_node)
                }
            }
            target_node_data = {
                'data': {
                    'id': target_node_id,
                    'label': list(target_node.labels)[0],
                    **dict(target_node)
                }
            }
            edge_data = {
                'data': {
                    'source': source_node_id,
                    'target': target_node_id,
                    'type': type(relationship).__name__,
                    **dict(relationship)
                }
            }

            if source_node_data not in nodes:
                nodes.append(source_node_data)
            if target_node_data not in nodes:
                nodes.append(target_node_data)
            if edge_data not in edges:
                edges.append(edge_data)

        return {'elements': nodes + edges}