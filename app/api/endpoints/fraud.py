from app.config.settings import settings
from fastapi import APIRouter, HTTPException
from app.database.neo4j_database import Neo4jDatabase
from app.models.community import CommunityModel
from typing import List

router = APIRouter()
graph_database = Neo4jDatabase()

@router.get("/shared-ip")
def detect_shared_ip(minutes: int = settings.high_velocity_ip_window_size):
    if minutes <= 0:
        raise HTTPException(status_code=400, detail="Minutes must be a positive integer")

    query = get_shared_ip_query(minutes)
    
    try:
        with graph_database.driver.session() as session:
            results = session.run(query, minutes=minutes)
            
            # Process the records and return the results
            shared_ip_results = [{
                "customer1": record["customer1"], 
                "customer2": record["customer2"],
                "ip_address": record["ip_address"]
            } for record in results]
        
        return {"results": shared_ip_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/risk-scores")
def calculate_risk_scores():
    query = get_risk_scores_query()
    
    try:
        with graph_database.driver.session() as session:
            result = session.run(query)
            records = result.data()
            
            risk_scores = [{"id": record["id"], "score": record["score"]} for record in records]
            
            return {"risk_scores": risk_scores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/community-detection", response_model=List[CommunityModel])
def detect_suspicious_communities(min_size: int = 5, min_density: float = 0.5, min_suspicion_score: float = 0.7):
    # Project the fraud graph with relevant node labels and relationship types
    project_query = """
        CALL gds.graph.project('fraud-graph', ['Customer', 'Device', 'IpAddress'], {
            PERFORMS: {
                orientation: 'UNDIRECTED'
            },
            USED: {
                orientation: 'UNDIRECTED'    
            }
        })
        YIELD graphName AS graph, nodeCount AS nodeCount, relationshipCount AS relationshipCount
    """
    with graph_database.driver.session() as session:
        session.run(project_query).consume()

    # Run the Louvain community detection algorithm
    detection_query = """
        CALL gds.louvain.stream('fraud-graph')
        YIELD nodeId, communityId
        RETURN gds.util.asNode(nodeId).id AS nodeId, communityId
    """
    with graph_database.driver.session() as session:
        results = list(session.run(detection_query))

    communities = {}
    for record in results:
        node_id = record["nodeId"]
        community_id = record["communityId"]
        if community_id not in communities:
            communities[community_id] = []
        communities[community_id].append(node_id)

    suspicious_communities = []
    for community_id, members in communities.items():
        size = len(members)
        if size >= min_size:
            # Calculate the community density
            subgraph_query = f"""
                MATCH (n)
                WHERE n.id IN {members}
                WITH collect(n) AS nodes
                UNWIND nodes AS n
                UNWIND nodes AS m
                RETURN sum(CASE WHEN (n)-[]-(m) THEN 1 ELSE 0 END) AS relationship_count
            """
            with graph_database.driver.session() as session:
                subgraph_result = session.run(subgraph_query).single()
                relationship_count = subgraph_result["relationship_count"]
            max_possible_relationships = size * (size - 1) / 2
            density = relationship_count / max_possible_relationships

            if density >= min_density:
                # Calculate the suspicion score based on domain knowledge and heuristics
                suspicion_score = calculate_suspicion_score(members)

                if suspicion_score >= min_suspicion_score:
                    community = CommunityModel(id=community_id, members=members, size=size, density=density, suspicion_score=suspicion_score)
                    suspicious_communities.append(community)

    return suspicious_communities

# HELPERS

def get_shared_ip_query(minutes: int):
    return """
        MATCH (c1:Customer)-[:USED]->(i:IpAddress)<-[:USED]-(c2:Customer)
        WHERE c1 <> c2
        AND c1.last_active_at > datetime() - duration({minutes: $minutes})
        AND c2.last_active_at > datetime() - duration({minutes: $minutes})
        RETURN c1.id AS customer1, c2.id AS customer2, i.id AS ip_address
    """

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

def calculate_suspicion_score(members: List[str]) -> float:
    # Implement the logic to calculate the suspicion score based on domain knowledge and heuristics
    # Example implementation:
    high_risk_customers = []
    for member in members:
        if is_high_risk_customer(member):
            high_risk_customers.append(member)
    suspicion_score = len(high_risk_customers) / len(members)
    return suspicion_score

def is_high_risk_customer(customer_id: str) -> bool:
    # Implement the logic to determine if a customer is high-risk based on predefined criteria
    # Example implementation:
    query = """
        MATCH (c:Customer {id: $customer_id})
        WHERE c.risk_score >= 0.8
        RETURN count(c) > 0 AS is_high_risk
    """
    with graph_database.driver.session() as session:
        result = session.run(query, customer_id=customer_id).single()
        return result["is_high_risk"]