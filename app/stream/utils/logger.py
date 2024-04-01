import logging

def log_agent_message(agent, topic, object, warning=None):
    if warning:
        _log_warning_message("AGENT", agent, topic, object, warning)
    else:
        _log_info_message("AGENT", agent, topic, object)

def log_timer_message(timer, topic, object, warning=None):
    if warning:
        _log_warning_message("TIMER", timer, topic, object, warning)
    else:
        _log_info_message("TIMER", timer, topic, object)


# ----------------------------------------------
# Helper functions
# ----------------------------------------------

def _log_info_message(actor_type, actor, topic, object):
    logging.info(f"""
    ***
    {actor_type}: {actor}
    TOPIC: {topic}
    TYPE: {object.__class__.__name__} ({object.type})
    IDENTIFIER: {object.uid}
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