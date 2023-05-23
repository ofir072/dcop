import random
import numpy as np
from agent import Agent

n = 5       # Number of agents in the network
k = 0.2     # The probability for pair of agents to be neighbors


def create_agents(num_of_agents):   # Create the agents objects in the current network
    agents = list()
    for i in range(1, num_of_agents + 1):
        agents.append(Agent(i))
    return agents


def generate_neighbors(network):    # Generate neighbors in the network
    for i in range(len(network)):
        for j in range(i + 1, len(network)):    # Loop other the remaining pairs for the upcoming agent
            if random.random() < k:   # Probability of neighbors filter
                matrix = np.array([[random.randint(0, 99) for _ in range(10)] for _ in range(10)])
                agent1 = network[i]
                agent2 = network[j]
                agent1.set_neighbors(agent2.agent_id, matrix)
                agent2.set_neighbors(agent1.agent_id, matrix.transpose())


network = create_agents(n)
generate_neighbors(network)

for agent in network:
    print(f"Agent ID: {agent.agent_id}")
    for neighbor_id, matrix in agent.neighbors.items():
        print(f"Neighbor ID: {neighbor_id}")
        for row in matrix:
            print(row)
        print()
    print("------")
