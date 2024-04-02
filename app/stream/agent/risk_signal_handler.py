"""
Risk Signal Handler Agents
"""

from app.stream.faust_app import faust_app
from app.stream.topic import risk_signal_topic
from app.database.neo4j_database import Neo4jDatabase
from app.models.v2 import RiskSignalType
from app.services import CustomerService, IpAddressService
from app.stream.util.loggers import agent_logger

graph_database = Neo4jDatabase()
customer_service = CustomerService(graph_database)
ip_address_service = IpAddressService(graph_database)

@faust_app.agent(risk_signal_topic)
async def risk_signal_handler(signals):
    async for signal in signals:
        if signal.type == RiskSignalType.LOGIN_VELOCITY:
            customer_service.mark_as_risky(
                uid=signal.event.customer.uid,
                reason=RiskSignalType.LOGIN_VELOCITY.value)
            agent_logger(
                "risk_signal_handler", 
                risk_signal_topic,
                signal)

        elif signal.type == RiskSignalType.IP_VELOCITY:
            ip_address_service.mark_as_risky(
                uid=signal.event.ip_address.uid,
                reason=RiskSignalType.IP_VELOCITY.value)
            agent_logger(
                "risk_signal_handler", 
                risk_signal_topic,
                signal)

        elif signal.type == RiskSignalType.APPLICATION_FRAUD:
            # @TODO: Implement.
            agent_logger(
                "risk_signal_handler", 
                risk_signal_topic,
                signal,
                warning="Not implemented")

        else:
            raise ValueError(f"Unknown signal type: {signal.type}")
