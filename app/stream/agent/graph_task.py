from app.stream.faust_app import faust_app
from app.stream.topic import graph_management_topic
from app.database.neo4j_database import Neo4jDatabase
from app.models import TaskEnum
from app.services import CustomerService
import logging

graph_database = Neo4jDatabase()
customer_service = CustomerService(graph_database)

@faust_app.agent(graph_management_topic)
async def process_customer_pii_link(tasks):
    async for task in tasks:
        if task.task == TaskEnum.CUSTOMER_PII_LINK:
            #@TODO: Implement the logic to link all customers with the same PII
            logging.info(f"Processed {TaskEnum.CUSTOMER_PII_LINK} graph task")
        else:
            raise ValueError(f"Unknown task type: {task.task}")