"""
Batch Jobs (Cron)
"""

from datetime import datetime
from uuid import uuid4
import logging
import pytz
from app.stream.faust_app import faust_app
from app.stream.topics import admin_task_topic
from app.models.admin import AdminTask, AdminTaskType


central = pytz.timezone('US/Central')


# Daily at 16:00 central time
@faust_app.crontab('16 00 * * *', timezone=central, on_leader=True)
async def link_customers_by_pii():
    logging.info('-- Job scheduled for: 16:00 Central time --')
    logging.info(f'Adding {AdminTaskType.LINK_CUSTOMERS_BY_PII.value} task at: {datetime.now()}')
    task = AdminTask(
        uid=uuid4(),
        task=AdminTaskType.LINK_CUSTOMERS_BY_PII,
        timestamp=int(datetime.now().timestamp()))
    await admin_task_topic.send(value=task)
