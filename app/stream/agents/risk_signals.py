from app.stream.faust_app import faust_app
from app.stream.topics import risk_signal_topic
from app.models import RiskSignal, RiskSignalType
from app.services import FraudService
from app.stream.utils.loggers import agent_logger
from app.database.manager import DatabaseManager
from app.database.repositories.graph import GraphRepository
from app.config.settings import settings


# ----------------------
# Init
# ----------------------

db_manager = DatabaseManager(settings)
graph_repo = GraphRepository(db_manager)
fraud_service = FraudService(graph_repo.db)

# ----------------------
# Agents
# ----------------------

def handle_login_velocity(signal:RiskSignal):
    fraud_service.process_fraud(signal)
    agent_logger("handler_login_velocity", risk_signal_topic, signal)


def handle_ip_velocity(signal:RiskSignal):
    fraud_service.process_fraud(signal)
    agent_logger("handler_ip_velocity", risk_signal_topic, signal)


def handle_application_fraud(signal:RiskSignal):
    fraud_service.process_fraud(signal)
    agent_logger("handle_application_fraud", risk_signal_topic, signal)


RISK_SIGNAL_HANDLERS = {
    RiskSignalType.LOGIN_VELOCITY: handle_login_velocity,
    RiskSignalType.IP_VELOCITY: handle_ip_velocity,
    RiskSignalType.APPLICATION_FRAUD: handle_application_fraud
}


@faust_app.agent(risk_signal_topic)
async def risk_signal_handler(signals):
    async for signal in signals:
        try:
            if not isinstance(signal, RiskSignal):
                raise TypeError("Expected RiskSignal, got {type(signal)}")
            else:
                handler = RISK_SIGNAL_HANDLERS[signal.signal_type]
                if handler is None:
                    raise ValueError(f"Invalid signal or handler. Signal: {signal}, Handler: {handler}")
                else:
                    handler(signal)
        except KeyError:
            agent_logger(
                "risk_signal_handler",
                risk_signal_topic, 
                signal, 
                warning=f"Unknown signal type: {signal.signal_type}"
            )
