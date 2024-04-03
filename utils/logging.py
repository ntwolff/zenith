import logging
from rich import print
from loguru import logger

def setup_logging():
    logger.add("app.log", rotation="1 MB", retention=10, enqueue=True)
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)

class InterceptHandler(logging.Handler):
    def emit(self, record):
        print(record.getMessage())
        #logger.info(record.getMessage()) @TODO: debug