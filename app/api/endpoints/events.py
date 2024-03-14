from fastapi import APIRouter, HTTPException
from app.models import CustomerEvent, CustomerEventModel
from app.processors import CustomerEventGraphProcessor
from app.api.endpoints import graph_database
import random

router = APIRouter()

@router.post("/customer-event", summary="Create a new CustomerEvent", response_model=None, status_code=201)
def create_customer_event(event: CustomerEventModel):
    """
    Create a new customer event.

    This endpoint allows you to create a new customer event by providing the necessary event details.

    - **event**: The customer event data including customer information, device information, and IP address.

    Returns:
    - A success message indicating that the event was processed successfully.

    Raises:
    - HTTPException (status_code=400): If the provided event data is invalid.
    """
    try:
        faust_event = CustomerEvent.from_model(event)
        processor = CustomerEventGraphProcessor(graph_database)
        processor.process(faust_event)
        return {"message": "Event processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/graph", summary="Get graph data for visualization")
def get_graph_data():
    """
    Get graph data for visualization.

    This endpoint retrieves graph data from the Neo4j database for visualization purposes.

    Returns:
    - A dictionary containing nodes and edges of the graph.
      - `elements`: A dictionary containing two lists:
        - `nodes`: A list of node objects, each containing:
          - `data`: Node data including `id`, `label`, and other properties.
          - `position`: Node position with `x` and `y` coordinates.
        - `edges`: A list of edge objects, each containing:
          - `data`: Edge data including `source`, `target`, `type`, and other properties.
          - `position`: Edge position with `x1`, `y1`, `x2`, `y2` coordinates.

    Raises:
    - HTTPException (status_code=500): If an error occurs while retrieving graph data from the database.
    """
    try:
        query = """
            MATCH (c:Customer)-[r]->(other)
            RETURN c, other, r
            LIMIT 200
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
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))