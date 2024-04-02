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

def _log_info_message(actor_type, actor, topic, obj:BaseModel):
    logging.info(f"""
    ***
    {actor_type}: {actor}
    TOPIC: {topic}
    TYPE: {obj.__class__.__name__} ({obj.type})
    IDENTIFIER: {obj.uid}
    ***""")


def _log_warning_message(actor_type, actor, topic, object, warning):
    logging.warning(f"""
    WARNING: {warning}
    ***
    {actor_type}: {actor}
    TOPIC: {topic}
    TYPE: {object.__class__.__name__} ({object.type})
    IDENTIFIER: {object.uid}
    ***""")
