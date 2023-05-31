import random
import numpy as np


class Agent:

    def __init__(self, agent_id, domain, communication_network):
        self.agent_id = agent_id
        self.domain = np.arange(1, domain)  # The range of the domain for the agent
        self.domain_choice = int(np.random.choice(self.domain, 1))  # The first random choice from the domain
        self.neighbors = {}
        self.communication_network = communication_network

    def set_neighbors(self, neighbor_id, matrix):  # Set neighbor info - costs matrix, current & next choice
        self.neighbors[neighbor_id] = {'matrix': matrix, 'base choice': None, 'next choice': None}

    # Update the neighbor new choice for next iteration
    def receive_message(self, neighbor_id, neighbor_choice, message_kind):
        for neighbor, neighbor_info in self.neighbors.items():
            if neighbor == neighbor_id:
                if message_kind == 'next':
                    neighbor_info['next choice'] = neighbor_choice
                elif message_kind == 'base':
                    neighbor_info['base choice'] = neighbor_choice
                else:
                    print("E-R-R-O-R-!")

    def send_choice_message(self):
        for neighbor_id, neighbor_info in self.neighbors.items():
            self.communication_network.send_message(self.agent_id, neighbor_id, self.domain_choice, "next")

    def dsa_make_choice(self, p):  # For the current neighbors choices make the best choice for this agent
        costs = {}
        if self.neighbors:      # Just agents that have neighbors can make new choice
            for choice in self.domain:  # Calculate the costs for given domain choice
                for neighbor, neighbor_info in self.neighbors.items():
                    neighbor_choice = neighbor_info['base choice']
                    matrix = neighbor_info['matrix']
                    if choice in costs:
                        costs[choice] += matrix[choice-1][neighbor_choice-1]  # Summing up the cost for all the agents
                    else:
                        costs[choice] = matrix[choice-1][neighbor_choice-1]   # First summing action
            if random.random() < p:
                self.domain_choice = min(costs, key=costs.get)      # For the minimum cost set the new choice
        self.send_choice_message()

    def update_next_iteration_choices(self):
        for neighbor, neighbor_info in self.neighbors.items():
            neighbor_info['base choice'] = neighbor_info['next choice']
            neighbor_info['next choice'] = 0
