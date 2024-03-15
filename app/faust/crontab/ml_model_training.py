from app.faust.app import faust_app
from app.ml.model_training import project_and_train_model
from app.config.settings import settings
import logging

@faust_app.crontab("0 0 * * *")  # Run every day at midnight
async def scheduled_ml_model_generation():
    logging.info("Running scheduled model generation")
    project_and_train_model(settings.neo4j_uri, settings.neo4j_user, settings.neo4j_password)