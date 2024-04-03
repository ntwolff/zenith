# ----------------------------------------------
# ALGORITHMS
# ----------------------------------------------
    
def page_rank(graph_name: str, limit: int = 10):
    return f"""
        CALL gds.pageRank.stream('{graph_name}')
        YIELD nodeId, score

        WITH gds.util.asNode(nodeId) AS node, score
        RETURN labels(node)[0] AS label, ID(node) as id, properties(node) as properties, score
        ORDER BY score DESC
        LIMIT {limit}
    """ 


# ----------------------------------------------
# UTIL CLASS
# ----------------------------------------------

class GraphHelper:
    algos = {
        "pageRank": page_rank
    }

    def create_graph(db, graph_name):
        query = f"""
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
        db.execute_query(query)

    def drop_graph(db, graph_name):
        query = f"CALL gds.graph.drop('{graph_name}', false) YIELD graphName"
        db.execute_query(query)

    def run_algorithm(db, algorithm, graph_name, limit=10):
        query = GraphHelper.algos[algorithm]
        return db.execute_query(query(graph_name=graph_name, limit=limit))
