import numpy as np


class Agent:

    def __init__(self, agent_id, domain):
        self.agent_id = agent_id
        self.domain = np.arange(1, domain)  # The range of the domain for the agent
        self.domain_choice = np.random.choice(self.domain, 1)  # The first random choice from the domain
        self.neighbors = {}

    def set_neighbors(self, neighbor_id, matrix, choice):  # Set neighbor info - costs matrix, current & next choice
        self.neighbors[neighbor_id] = {'matrix': matrix, 'base choice': choice, 'next choice': None}

    def share_choice(self):  # Return a list of agents ids that need to be updated for his new choice
        neighbors_ids = list()
        for neighbor in self.neighbors.items():
            neighbors_ids.append(neighbor)
        return neighbors_ids

    def update_neighbor_choice(self, neighbor_id, neighbor_choice):  # Update the neighbor new choice for next iteration
        for neighbor, neighbor_info in self.neighbors.items():
            if neighbor == neighbor_id:
                neighbor_info['next choice'] = neighbor_choice

    def make_choice(self):  # For the current neighbors choices make the best choice for this agent
        costs = {}
        if self.neighbors:      # Just agents that have neighbors can make new choice
            for choice in self.domain:  # Calculate the costs for given domain choice
                for neighbor, neighbor_info in self.neighbors.items():
                    neighbor_choice = neighbor_info['base choice']
                    matrix = neighbor_info['matrix']
                    if choice in costs:
                        costs[choice-1] += matrix[choice-1][neighbor_choice-1]  # Summing up the cost for all the agents
                    else:
                        costs[choice-1] = matrix[choice-1][neighbor_choice-1]   # First summing action
            self.domain_choice = min(costs, key=costs.get)      # For the minimum cost set the new choice
        else:
            print("No constraints - base choice remain!")
