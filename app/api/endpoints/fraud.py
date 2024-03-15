from fastapi import APIRouter, HTTPException
from app.database.neo4j_database import Neo4jDatabase
from app.models.community import CommunityModel

router = APIRouter()
graph_database = Neo4jDatabase()

# @TODO: Migrate to graph data science library (https://neo4j.com/docs/graph-data-science-client/current/)

@router.get("/page-rank", summary="Get page rank scores", response_model=dict)
def get_page_rank(limit: int = 25):
    """
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


@router.get("/centrality", summary="Get centrality scores", response_model=dict)
def get_centrality_scores(limit: int = 25):
    """
    Get centrality scores of nodes in the graph.

    This endpoint retrieves centrality scores of nodes in the graph using the Neo4j Graph Data Science library.

    Parameters:
    - **limit**: The maximum number of centrality scores to return (default: 25).

    Returns:
    - A dictionary containing centrality scores of nodes.
      - `centrality_scores`: A list of objects, each containing:
        - `id`: The ID of the node.
        - `centrality`: The centrality score of the node.

    Raises:
    - HTTPException (status_code=500): If an error occurs while calculating centrality scores.
    """
    query = get_centrality_scores_query(limit)

    try:
        with graph_database.driver.session() as session:
            session.run(drop_fraud_graph_query())
            session.run(project_fraud_graph_query())

            results = session.run(query)
            return {"centrality_scores": [dict(record) for record in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/communities", summary="Detect suspicious communities")
def detect_suspicious_communities(min_size: int = 5, min_density: float = 0.5, min_suspicion_score: float = 0.7):
    """
    Detect suspicious communities in the graph.

    This endpoint detects suspicious communities in the graph using community detection algorithms and suspicion scoring.

    - **min_size**: The minimum size of a community to be considered suspicious (default: 5).
    - **min_density**: The minimum density of a community to be considered suspicious (default: 0.5).
    - **min_suspicion_score**: The minimum suspicion score of a community to be considered suspicious (default: 0.7).

    Returns:
    - A list of suspicious community objects, each containing:
      - `id`: The ID of the community.
      - `members`: A list of member node IDs in the community.
      - `size`: The number of members in the community.
      - `density`: The density of the community.
      - `suspicion_score`: The suspicion score of the community.

    Raises:
    - HTTPException (status_code=500): If an error occurs while detecting suspicious communities.
    """
    try:
        with graph_database.driver.session() as session:
            return {"message": "Not implemented yet"}

            # @TODO: Revise community detection query

            session.run(drop_fraud_graph_query())
            session.run(project_fraud_graph_query())

            results = session.run(get_community_detection_query())
            return {"communities": [dict(record) for record in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


def get_centrality_scores_query(limit: int = 25):
    return f"""
        CALL gds.degree.stream('fraud-graph')
        YIELD nodeId, score

        WITH gds.util.asNode(nodeId) AS node, score
        RETURN labels(node)[0] AS label, ID(node) as id, properties(node) as properties, score    
        ORDER BY score DESC
        LIMIT {limit}
    """


def get_community_detection_query():
    query = """
        CALL gds.louvain.stream('fraud-graph')
        YIELD nodeId, communityId

        WITH communityId, collect(gds.util.asNode(nodeId)) AS nodes
        WHERE size(nodes) >= 5

        WITH communityId, nodes, size(nodes) AS communitySize

        CALL gds.localClusteringCoefficient.stream('fraud-graph', {nodeLabels: ['Customer', 'Device', 'IpAddress', 'Address']})
        YIELD nodeId, localClusteringCoefficient

        WITH communityId, communitySize, nodes, avg(localClusteringCoefficient) AS communityDensity
        WHERE communityDensity > 0.0005

        MATCH (c:Customer)
        WHERE ANY(node IN nodes WHERE c.customer_id = node.customer_id)
        WITH communityId, communitySize, communityDensity, nodes, count(c) AS customerCount

        RETURN communityId,
            [node IN nodes] AS members,
            communitySize,
            communityDensity,
            customerCount * 1.0 / communitySize AS customerRatio
        ORDER BY communitySize DESC, communityDensity DESC, customerRatio DESC
    """
    return query