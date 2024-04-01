from app.stream.faust_app import faust_app
from app.stream.topic import risk_signal_topic
from app.database.neo4j_database import Neo4jDatabase
from app.models.v2 import RiskSignalType
from app.services import CustomerService, IpAddressService
import logging

graph_database = Neo4jDatabase()
customer_service = CustomerService(graph_database)
ip_address_service = IpAddressService(graph_database)

@faust_app.agent(risk_signal_topic)
async def handle_risk_signal(signals):
    async for signal in signals:
        if signal.type == RiskSignalType.LOGIN_VELOCITY:
            customer_service.mark_as_risky(
                uid=signal.event.customer.uid, 
                reason=RiskSignalType.LOGIN_VELOCITY.value)
            
            logging.info(f"Processed {RiskSignalType.LOGIN_VELOCITY.value} risk signal for customer: {signal.event.customer.uid}")    
        
        elif signal.type == RiskSignalType.IP_VELOCITY:
            ip_address_service.mark_as_risky(
                uid=signal.event.ip_address.uid, 
                reason=RiskSignalType.IP_VELOCITY.value)
            
            logging.info(f"Processed {RiskSignalType.IP_VELOCITY.value} risk signal for ip address: {signal.event.ip_address.ipv4}") 
        
        elif signal.type == RiskSignalType.APPLICATION_FRAUD:
            # @TODO: Implement.

            logging.info("Application fraud signal received.  Not yet implemented.") 
        
        else:
            raise ValueError(f"Unknown signal type: {signal.type}")