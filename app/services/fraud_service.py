from app.models import FraudStatus, RiskSignal
from app.services.base import GraphService

class FraudStateMachine:
    def __init__(self, initial_state=FraudStatus.UNKNOWN):
        self.state = initial_state

    def transition_to(self, new_state):
        valid_transitions = {
            FraudStatus.UNKNOWN: [FraudStatus.SUSPECTED, FraudStatus.CLEARED],
            FraudStatus.SUSPECTED: [FraudStatus.CONFIRMED, FraudStatus.CLEARED],
            FraudStatus.CONFIRMED: [FraudStatus.CLEARED],
            FraudStatus.CLEARED: [FraudStatus.SUSPECTED],
        }

        if new_state in valid_transitions[self.state]:
            self.state = new_state
        elif new_state == self.state:
            pass
        else:
            #raise ValueError(f"Invalid transition from {self.state} to {new_state}") @TODO: Fake logic
            pass


class FraudService(GraphService):
    def __init__(self, db):
        super().__init__(db)
        self.state_machine = FraudStateMachine()

    def process_fraud(self, signal: RiskSignal):
        if signal.fraud_score > 0.8:
            self.state_machine.transition_to(FraudStatus.CONFIRMED) #@TODO: Fake logic
        elif signal.fraud_score > 0.5:
            self.state_machine.transition_to(FraudStatus.SUSPECTED)
        else:
            self.state_machine.transition_to(FraudStatus.CLEARED)

        self.update_event_fraud_status(signal.event, self.state_machine.state)

    def update_event_fraud_status(self, event, fraud_status):
        event.fraud_status = fraud_status
        #self.db.update_event(event) @TODO: Implement

    def get_fraud_status(self, event):
        return event.fraud_status

    def mark_as_confirmed_fraud(self, event):
        self.state_machine.transition_to(FraudStatus.CONFIRMED)
        self.update_event_fraud_status(event, FraudStatus.CONFIRMED)

    def mark_as_cleared(self, event):
        self.state_machine.transition_to(FraudStatus.CLEARED)
        self.update_event_fraud_status(event, FraudStatus.CLEARED)