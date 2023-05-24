import random
import numpy as np
from agent import Agent


n = 4           # Number of agents in the network
k = 0.2         # The probability for pair of agents to be neighbors
domain = 3      # Size of domain for all the agents
cost = 3        # The maximum cost for placement of two agents decision


def create_agents(num_of_agents):   # Create the agents objects in the current network
    agents = list()
    for i in range(1, num_of_agents + 1):
        agents.append(Agent(i, domain+1))
    return agents


def generate_neighbors(network):    # Generate neighbors in the network
    for i in range(len(network)):
        for j in range(i + 1, len(network)):    # Loop other the remaining pairs for the upcoming agent
            if random.random() < k:   # Probability of neighbors filter
                matrix = np.array([[random.randint(0, cost) for _ in range(domain)] for _ in range(domain)])
                agent1 = network[i]
                agent2 = network[j]
                agent1.set_neighbors(agent2.agent_id, matrix, agent2.domain_choice)
                agent2.set_neighbors(agent1.agent_id, matrix.transpose(), agent1.domain_choice)


network = create_agents(n)
generate_neighbors(network)

for agent in network:
    print(f"Agent ID: {agent.agent_id}")
    print(f"Agent Domain: {agent.domain}")
    print(f"Agent Choice: {agent.domain_choice}")
    for neighbor_id, neighbor_info in agent.neighbors.items():
        print(f"Neighbor ID: {neighbor_id}")
        print(f"Neighbor base choice: {neighbor_info['base choice']}")
        print(f"Neighbor next choice: {neighbor_info['next choice']}")
        matrix = neighbor_info['matrix']
        for row in matrix:
            print(row)
        print()
    print("------")

for agent in network:
    agent.make_choice()
    print(f"Agent ID: {agent.agent_id}")
    print(f"Agent Choice: {agent.domain_choice}")
