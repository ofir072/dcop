import random
import numpy as np


class Agent:

    def __init__(self, agent_id, domain, communication_network):
        self.agent_id = agent_id
        self.domain = np.arange(1, domain)                           # The range of the domain for the agent
        self.domain_choice = int(np.random.choice(self.domain, 1))   # The first random choice from the domain
        self.next_choice = None                                      # Save the best choice for the next move in MGM
        self.loc_red = -1                                            # Set the initial local reduction to unsafe value
        self.neighbors = {}                                          # Neighbors dictionary
        self.communication_network = communication_network           # Communication network for messages exchanges

    def set_neighbors(self, neighbor_id, matrix):  # Set neighbor info - costs matrix, current & next choice
        self.neighbors[neighbor_id] = {'matrix': matrix, 'base choice': None, 'next choice': None, 'LR value': None}

    def receive_message(self, neighbor_id, neighbor_message, message_kind):  # Message arrived by communication network
        for neighbor, neighbor_info in self.neighbors.items():
            if neighbor == neighbor_id:         # Find the sending agent in the neighbors dictionary
                if message_kind == 'next':      # Next choice of neighbor message
                    neighbor_info['next choice'] = neighbor_message
                elif message_kind == 'base':    # Base choice of neighbor message
                    neighbor_info['base choice'] = neighbor_message
                else:                           # Local reduction of neighbor message
                    neighbor_info['LR value'] = neighbor_message

    def send_message(self, message_type):  # Send message to all the agents with the info type by communication network
        for neighbor_id, neighbor_info in self.neighbors.items():
            if message_type == "base":      # Base choice of agent message
                self.communication_network.send_message(self.agent_id, neighbor_id, self.domain_choice, "base")
            elif message_type == "next":    # Next choice of agent message
                self.communication_network.send_message(self.agent_id, neighbor_id, self.domain_choice, "next")
            elif message_type == "LR":      # Local reduction of agent message
                self.communication_network.send_message(self.agent_id, neighbor_id, self.loc_red, "lr")

    def info_update_next_iteration(self, kind):    # The communication network inform that iteration ends - update data
        self.next_choice = None
        for neighbor, neighbor_info in self.neighbors.items():
            if kind == "MGM":   # Reset for MGM algorithm - LR values and next choice
                self.next_choice = None
                self.loc_red = -1
                neighbor_info['LR value'] = -1
            else:               # Reset for DSA-C algorithm - base and next choices
                neighbor_info['base choice'] = neighbor_info['next choice']
                neighbor_info['next choice'] = 0

    def dsa_make_choice(self, p):  # For the current neighbors choices make the best choice for this agent
        costs = {}
        if self.neighbors:      # Just agents that have neighbors can make new choice
            for choice in self.domain:      # Calculate the costs for given domain choice
                for neighbor, neighbor_info in self.neighbors.items():
                    neighbor_choice = neighbor_info['base choice']
                    matrix = neighbor_info['matrix']
                    if choice in costs:
                        costs[choice] += matrix[choice-1][neighbor_choice-1]  # Summing up the cost for all the agents
                    else:
                        costs[choice] = matrix[choice-1][neighbor_choice-1]   # First summing action
            if random.random() < p:
                self.domain_choice = min(costs, key=costs.get)      # For the minimum cost set the new choice
        self.send_message("next")

    def mgm_set_local_reduction(self):
        reduction = {}
        if self.neighbors:      # Just agents that have neighbors can calculate local reduction
            for red in self.domain:      # Calculate the local reduction for given domain choice
                for neighbor, neighbor_info in self.neighbors.items():
                    neighbor_choice = neighbor_info['base choice']
                    matrix = neighbor_info['matrix']
                    if red in reduction:
                        reduction[red] += matrix[red-1][neighbor_choice-1]  # Sum the reduction cost for all the agents
                    else:
                        reduction[red] = matrix[red-1][neighbor_choice-1]   # First summing action for this choice
            current_choice = reduction[self.domain_choice]
            for red in self.domain:     # Evaluate the LR with the total cost of the current choice for each choice
                reduction[red] = current_choice - reduction[red]
            # Gets the best local reduction from the list and the choice that made it
            self.next_choice = max(reduction, key=reduction.get)
            self.loc_red = max(reduction.values())
        self.send_message("LR")     # Update all the neighbor about the local reduction the agent found

    def mgm_make_choice(self):  # Search for the maximum LR among the agent neighbors - and make choice if he holds max
        make_choice = True
        if self.neighbors and self.loc_red > 0:      # Agents that have neighbors and LR positive can make new choice
            for neighbor, neighbor_info in self.neighbors.items():
                # There is a neighbor with higher local reduction
                if self.loc_red < neighbor_info['LR value']:
                    make_choice = False
                # There is a neighbor with the maximum reduction like the agent but his index is before the agent
                if self.loc_red <= neighbor_info['LR value'] and self.agent_id > neighbor:
                    make_choice = False
            if make_choice is True:
                # The agent holds the max reduction - update his base choice and send to all the neighbors the choice
                self.domain_choice = self.next_choice
                self.send_message("base")
