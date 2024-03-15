from app.faust.app import faust_app
from app.faust.topic import risk_signal_topic
from app.database.neo4j_database import Neo4jDatabase
from app.models import SignalEnum
from app.services import CustomerService, IpAddressService
import logging

graph_database = Neo4jDatabase()
customer_service = CustomerService(graph_database)
ip_address_service = IpAddressService(graph_database)

@faust_app.agent(risk_signal_topic)
async def mitigate_risk_signal(signals):
    async for signal in signals:
        if signal.signal == SignalEnum.LOGIN_VELOCITY.value:
            customer_service.mark_as_risky(customer_id=signal.event.customer.customer_id, reason=SignalEnum.LOGIN_VELOCITY)
            logging.info(f"Processed {SignalEnum.LOGIN_VELOCITY} risk signal for customer: {signal.event.customer.customer_id}")    
        elif signal.signal == SignalEnum.IP_VELOCITY.value:
            ip_address_service.mark_as_risky(ip_address_id=signal.event.ip_address.ip_address_id, reason=SignalEnum.IP_VELOCITY.value)
            logging.info(f"Processed {SignalEnum.IP_VELOCITY.value} risk signal for customer: {signal.event.ip_address.ip_address_id}") 
        elif signal.signal == SignalEnum.APPLICATION_FRAUD.value:
            logging.info("Application fraud signal received.  Not yet implemented.") # @TODO: Implement.
        else:
            raise ValueError(f"Unknown signal type: {signal.signal}")