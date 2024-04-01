# from app.config.settings import settings
# from app.stream.faust_app import faust_app
# from app.stream.topic import event_topic, risk_signal_topic
# from app.models import RiskSignal, SignalEnum
# from app.ml.model_deployment import load_model
# from app.database.neo4j_database import Neo4jDatabase
# from uuid import uuid4
# import logging

# fraud_detection_model = None
# graph_database = Neo4jDatabase()

# def get_customer_features(customer_uid):
#     query = """
#     MATCH (c:Customer {uid: $customer_uid})
#     RETURN c.degree AS degree, c.pagerank AS pagerank, c.embedding AS embedding
#     """
#     result = graph_database.execute_query(query, uid=customer_uid)
#     record = result.single()
#     return {
#         "degree": record["degree"],
#         "pagerank": record["pagerank"],
#         "embedding": record["embedding"]
#     }

# @faust_app.agent(event_topic)
# async def detect_application_fraud(events):
#     global fraud_detection_model

#     if not settings.ml_detection_enabled:
#         return
#     elif fraud_detection_model is None:
#         fraud_detection_model = load_model("models/fraud_detection_model.pkl")
#         if not fraud_detection_model:
#             logging.error("Failed to load fraud detection model")
#             return

#     async for event in events:
#         features = get_customer_features(event.customer.uid)
#         prediction = fraud_detection_model.predict(features)
#         if prediction == 1:
#             logging.info(f"Application flagged as potentially fraudulent: {event.application.uid}")
#             payload = RiskSignal(
#                 uid=uuid4(),
#                 signal=SignalEnum.APPLICATION_FRAUD,
#                 event=event
#             )
#             await risk_signal_topic.send(value=payload)