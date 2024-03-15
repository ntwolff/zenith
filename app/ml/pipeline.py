from graphdatascience import GraphDataScience
from app.config.settings import settings

#gds = GraphDataScience("neo4j+s://my-aura-ds.databases.neo4j.io:7687", auth=("neo4j", "my-password"), aura_ds=True)
gds = GraphDataScience(settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password), aura_ds=False)

def create_fraud_detection_pipeline(gds):
    print(gds.version())
    assert gds.version()

    pipeline = gds.beta.pipeline.nodeClassification.create("fraud-detection-pipeline")

    # Add node properties as features
    pipeline.addNodeProperty("degree", mutateProperty="degree")
    pipeline.addNodeProperty("pagerank", mutateProperty="pagerank")
    pipeline.addNodeProperty("embedding", mutateProperty="embedding")
    pipeline.selectFeatures(["degree", "pagerank", "embedding"])

    # Add a Random Forest classifier
    pipeline.addRandomForest(maxDepth=10, numberOfDecisionTrees=100)

    return pipeline

def train_fraud_detection_model(gds, pipeline, graph_name, target_property):
    model, train_result = pipeline.train(
        graph_name,
        modelName="fraud-detection-model",
        targetProperty=target_property,
        metrics=["ACCURACY", "PRECISION", "RECALL", "F1_SCORE"],
    )

    print(f"Training Results: {train_result}")
    print(f"Model Metrics: {model.metrics()}")

    return model