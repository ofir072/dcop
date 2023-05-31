
class Communication_Network:
    def __init__(self):
        self.network = list()

    def send_message(self, sending_agent, receiving_agent, message, message_kind):
        for agent in self.network:
            if agent.agent_id == receiving_agent:
                agent.receive_message(sending_agent, message, message_kind)
