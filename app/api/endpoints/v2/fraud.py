"""
Fraud API endpoints

***

@TODO: 
- Migrate to GDS Python library
"""

from fastapi import APIRouter, HTTPException
from app.database.neo4j_database import Neo4jDatabase

# Initialize router and graph database
router = APIRouter()
graph_database = Neo4jDatabase()


@router.get("/page-rank", summary="Get page rank scores", response_model=dict)
def get_page_rank(limit: int = 25):
    """
    Demonstration of Neo4j GDS via the Page Rank algorithm.

    ***

    Get the page rank scores of nodes in the graph.

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
    graph_name = "fraud_graph"
    query = get_page_rank_scores_query(graph_name, limit)

    try:
        with graph_database.driver.session() as session:
            session.run(drop_fraud_graph_query(graph_name))
            session.run(project_fraud_graph_query(graph_name))

            result = session.run(query)
            records = result.data()

            risk_scores = [{
                "label": record["label"], "id": record["id"], "properties": record["properties"], 
                "score": record["score"]} for record in records]

            return {"page_rank_scores": risk_scores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}") from e


# ----------------------------------------------
# Helper functions
# ----------------------------------------------

def drop_fraud_graph_query(graph_name: str):
    """
    Drop the fraud graph if it exists.
    """

    return f"CALL gds.graph.drop('{graph_name}', false) YIELD graphName"


def project_fraud_graph_query(graph_name: str):
    """
    Create a fraud graph projection.
    """

    return f"""
        CALL gds.graph.project('{graph_name}', ['Customer', 'Device', 'IpAddress', 'Address'], {{
            PERFORMS: {{
                orientation: 'UNDIRECTED'
            }},
            USED: {{
                orientation: 'UNDIRECTED'    
            }},
            SHARES_PII: {{
                orientation: 'UNDIRECTED'
            }}
        }})
        YIELD graphName AS graph, nodeProjection AS nodes, relationshipProjection AS rels
    """


def get_page_rank_scores_query(graph_name: str, limit: int = 25):
    """
    Get the page rank scores of nodes in the graph.
    """

    return f"""
        CALL gds.pageRank.stream('{graph_name}')
        YIELD nodeId, score

        WITH gds.util.asNode(nodeId) AS node, score
        RETURN labels(node)[0] AS label, ID(node) as id, properties(node) as properties, score
        ORDER BY score DESC
        LIMIT {limit}
    """
