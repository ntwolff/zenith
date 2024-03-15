from app.database.neo4j_database import Neo4jDatabase
from graphdatascience import GraphDataScience
from app.ml.pipeline import create_fraud_detection_pipeline, train_fraud_detection_model
from app.ml.model_deployment import save_model

def project_and_train_model(uri, user, password):
    driver = Neo4jDatabase(uri, user, password).driver
    gds = GraphDataScience(driver, aura_ds=True)

    # Project the graph
    gds.run_cypher(
        """
        MATCH (c:Customer)-[:PERFORMS]->(e:Event)-[:HAS]->(d:Device)
        MATCH (e)-[:HAS]->(i:IpAddress)
        RETURN id(c) AS customer_id, c.is_fraud AS is_fraud, id(d) AS device_id, id(i) AS ip_address_id
        """
    )
    G, project_result = gds.graph.project(
        "fraud_graph",
        {"Customer": {"properties": ["is_fraud"]}, "Device": {}, "IpAddress": {}},
        {"PERFORMS": {}, "HAS": {}}
    )

    # Create the fraud detection pipeline
    pipeline = create_fraud_detection_pipeline(gds)

    # Train the model
    model = train_fraud_detection_model(gds, pipeline, "fraud_graph", "is_fraud")

    # Save the trained model
    save_model(model, "models/fraud_detection_model.pkl")

    driver.close()