
def message_arrived(network, receiving_agent, sending_agent, message):
    for agent in network:
        if agent.agent_id == receiving_agent:
            agent.update_neighbor_choice(sending_agent, message)