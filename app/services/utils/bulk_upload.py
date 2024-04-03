import pandas as pd
from app.models import Event
from app.config.settings import settings
from app.database.manager import DatabaseManager
from app.database.repositories.graph import GraphRepository

db_manager = DatabaseManager(settings)
graph_repo = GraphRepository(db_manager)

class BulkEventUploadService:
    async def process_file(self, file):
        data = pd.read_csv(file)
        db = graph_repo.db
        for _, row in data.iterrows():
            event = Event(**row.to_dict())
            db.add(event)
        db.commit()