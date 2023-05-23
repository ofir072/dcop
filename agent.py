class Agent:

    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.domain_choice = None
        self.agent_choices = []
        self.neighbors = {}

    def set_neighbors(self, neighbor_id, matrix):
        self.neighbors[neighbor_id] = matrix
