"""
Faust Agents - Administrative Tasks
"""

from app.stream.faust_app import faust_app
from app.stream.topics import admin_task_topic
from app.database.neo4j_database import Neo4jDatabase
from app.models import AdminTaskType
from app.services import CustomerService
from app.stream.utils.loggers import agent_logger

# ----------------------
# Db Initialization
# ----------------------

graph_database = Neo4jDatabase()
customer_service = CustomerService(graph_database)


# ----------------------
# Agent Definitions
# ----------------------

@faust_app.agent(admin_task_topic)
async def admin_task_handler(tasks):
    async for task in tasks:
        if task.task_type == AdminTaskType.CUSTOMER_PII_LINK:
            #@TODO: Implement.
            agent_logger("admin_task_handler", admin_task_topic, task)
        else:
            raise ValueError(f"Unknown task type: {task.task_type}")
