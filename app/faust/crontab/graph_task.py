from app.faust.app import faust_app
from app.faust.topic import graph_management_topic
from app.models import GraphTask, TaskEnum
from datetime import datetime
from uuid import uuid4
import pytz
import logging

central = pytz.timezone('US/Central')

# 8:20 PM Central time
@faust_app.crontab('16 00 * * *', timezone=central, on_leader=True)
async def link_customers_by_pii():
    logging.info('-- This should be run at 20:00 Central time --')
    logging.info(f'Adding {TaskEnum.LINK_CUSTOMERS_BY_PII} task at: {datetime.now()}')
    task = GraphTask(uid=uuid4(), task=TaskEnum.LINK_CUSTOMERS_BY_PII, timestamp=int(datetime.now().timestamp()))
    await graph_management_topic.send(value=task)