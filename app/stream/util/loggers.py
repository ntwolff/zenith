"""
Stream Logging Utilities
"""

import logging
from pydantic import BaseModel

def agent_logger(agent, topic, obj:BaseModel, warning=None):
    if warning:
        _log_warning_message("AGENT", agent, topic, obj, warning)
    else:
        _log_info_message("AGENT", agent, topic, obj)

def timer_logger(timer, topic, obj, warning=None):
    if warning:
        _log_warning_message("TIMER", timer, topic, obj, warning)
    else:
        _log_info_message("TIMER", timer, topic, obj)


# ----------------------------------------------
# Helper functions
# ----------------------------------------------

def _log_info_message(actor_type, actor, topic, model:BaseModel):
    logging.info(f"""
    ***
    {actor_type}: {actor}
    TOPIC: {topic}
    TYPE: {model.__class__.__name__} ({model.type})
    IDENTIFIER: {model.uid}
    ***""")


def _log_warning_message(actor_type, actor, topic, model:BaseModel, warning):
    logging.warning(f"""
    WARNING: {warning}
    ***
    {actor_type}: {actor}
    TOPIC: {topic}
    TYPE: {model.__class__.__name__} ({model.type})
    IDENTIFIER: {model.uid}
    ***""")
