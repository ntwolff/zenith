from app.config.settings import settings
from fastapi import APIRouter, HTTPException
from app.database.neo4j_database import Neo4jDatabase
from app.models.community import CommunityModel
import uuid

router = APIRouter()
graph_database = Neo4jDatabase()

@router.get("/page-rank")
def get_page_rank():
    query = get_risk_scores_query()
    
    try:
        with graph_database.driver.session() as session:
            result = session.run(query)
            records = result.data()
            
            risk_scores = [{"id": record["id"], "score": record["score"]} for record in records]
            
            return {"risk_scores": risk_scores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/centrality")
def get_centrality_scores():
    graph_name = f"fraud-graph-{uuid.uuid4()}"

    query = f"""
        CALL gds.graph.project('{graph_name}', 'Customer', 'SHARES_PII')
        YIELD graphName AS graph, nodeCount AS nodes, relationshipCount AS rels

        CALL gds.degree.stream('{graph_name}')
        YIELD nodeId, score
        RETURN gds.util.asNode(nodeId).id AS id, score AS centrality
        ORDER BY centrality DESC
    """
    with graph_database.driver.session() as session:
        results = session.run(query)
        return {"centrality_scores": [dict(record) for record in results]}

@router.get("/communities")
def detect_communities():
    # Project the graph
    project_query = """
        CALL gds.graph.project(
            'fraud-graph',
            'Customer',
            {
                SHARES_PII: {
                    orientation: 'UNDIRECTED'
                },
                USED: {
                    orientation: 'UNDIRECTED'
                }
            }
        )
    """
    with graph_database.driver.session() as session:
        session.run(project_query)

    # Run the community detection algorithm
    detection_query = """
        CALL gds.louvain.stream('fraud-graph')
        YIELD nodeId, communityId
        RETURN gds.util.asNode(nodeId).id AS id, communityId
    """
    with graph_database.driver.session() as session:
        results = session.run(detection_query)
        return {"communities": [dict(record) for record in results]}

# HELPERS

def get_risk_scores_query():
    return """
        CALL gds.graph.project('fraud-graph', ['Customer', 'Device', 'IpAddress'], {
            PERFORMS: {
                orientation: 'UNDIRECTED'
            },
            USED: {
                orientation: 'UNDIRECTED'    
            }
        })
        YIELD graphName AS graph, nodeProjection AS nodes, relationshipProjection AS rels
        
        CALL gds.pageRank.stream(graph)
        YIELD nodeId, score
        RETURN gds.util.asNode(nodeId).id AS id, score
        ORDER BY score DESC
    """