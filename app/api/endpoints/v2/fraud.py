from fastapi import APIRouter, HTTPException
from app.database.neo4j_database import Neo4jDatabase

"""
Fraud related endpoints for yielding insights from the graph.

@TODO: Migrate to graph data science library (https://neo4j.com/docs/graph-data-science-client/current/)
"""

# Initialize router and graph database
router = APIRouter()
graph_database = Neo4jDatabase()


@router.get("/page-rank", summary="Get page rank scores", response_model=dict)
def get_page_rank(limit: int = 25):
    """
    ***Demonstrative of Neo4j Graph Data Science functionality***

    Get the page rank scores of nodes in the graph.  
    
    This endpoint retrieves page rank scores of nodes in the graph using the Neo4j Graph Data Science library.
    Considers nodes of types: Customer, Device, IpAddress, Address.

    Parameters:
    - **limit**: The maximum number of page rank scores to return (default: 25).

    Returns:
    - A dictionary containing page rank scores of nodes.
      - `page_rank_scores`: A list of objects, each containing:
        - `id`: The ID of the node.
        - `score`: The page rank score of the node.

    Raises:
    - HTTPException (status_code=500): If an error occurs while calculating centrality scores.
    """
    query = get_page_rank_scores_query(limit)
    
    try:
        with graph_database.driver.session() as session:
            session.run(drop_fraud_graph_query())
            session.run(project_fraud_graph_query())

            result = session.run(query)
            records = result.data()
            
            risk_scores = [{"label": record["label"], "id": record["id"], "properties": record["properties"], "score": record["score"]} for record in records]
            
            return {"page_rank_scores": risk_scores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

# ----------------------------------------------
# Helper functions
# ----------------------------------------------

def drop_fraud_graph_query(graph_name: str = "fraud-graph"):
    return f"CALL gds.graph.drop('{graph_name}', false) YIELD graphName"


def project_fraud_graph_query(graph_name: str = "fraud-graph"):
    return """
        CALL gds.graph.project('fraud-graph', ['Customer', 'Device', 'IpAddress', 'Address'], {
            PERFORMS: {
                orientation: 'UNDIRECTED'
            },
            USED: {
                orientation: 'UNDIRECTED'    
            },
            SHARES_PII: {
                orientation: 'UNDIRECTED'
            }
        })
        YIELD graphName AS graph, nodeProjection AS nodes, relationshipProjection AS rels
    """


def get_page_rank_scores_query(limit: int = 25):
    return f"""
        CALL gds.pageRank.stream('fraud-graph')
        YIELD nodeId, score

        WITH gds.util.asNode(nodeId) AS node, score
        RETURN labels(node)[0] AS label, ID(node) as id, properties(node) as properties, score
        ORDER BY score DESC
        LIMIT {limit}
    """