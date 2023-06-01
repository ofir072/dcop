
class Communication_Network:
    def __init__(self):
        self.network = list()   # All the agents that in this communication network

    def send_message(self, sending_agent, receiving_agent, message, message_kind):  # Connect message to receiving agent
        for agent in self.network:
            if agent.agent_id == receiving_agent:   # Search for the receiving agent
                agent.receive_message(sending_agent, message, message_kind)

    def initialization_iteration(self, kind):  # Tell every agent in the network to reset his neighbors information
        for network_agent in self.network:
            network_agent.info_update_next_iteration(kind)
