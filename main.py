import random
import numpy as np
import communicationNetwork
from agent import Agent
import pandas as pd
import matplotlib.pyplot as plt


n = 30              # Number of agents in the network
k1 = 0.2            # The probability for pair of agents to be neighbors
k2 = 0.7            # The probability for pair of agents to be neighbors
p1 = 0.2            # The probability of an agent to make his next choice
p2 = 0.7            # The probability of an agent to make his next choice
domain = 10         # Size of domain for all the agents
cost = 99           # The maximum cost for placement of two agents decision
runs = 30           # Number of runs for each simulation
rounds = 30         # Number of rounds for each p value
iterations = 1000   # Number of iterations for the algorithms comparison part


def create_agents(communication_network, num_of_agents):   # Create the agents objects in the current network
    all_agents = list()
    for i in range(1, num_of_agents + 1):
        new_agent = Agent(i, domain+1, communication_network)
        all_agents.append(new_agent)
        communication_network.network.append(new_agent)     # Add all the agents to the communication network
    return all_agents


def generate_neighbors(network, probability, upper_cost):    # Generate neighbors in the network
    for i in range(len(network)):
        for j in range(i + 1, len(network)):    # Loop other the remaining pairs for the upcoming agent
            if random.random() < probability:   # Probability of neighbors filter
                # Matrix uniq creation for pair neighbor
                matrix = np.array([[random.randint(0, upper_cost) for _ in range(domain)] for _ in range(domain)])
                agent1 = network[i]
                agent2 = network[j]
                agent1_id = agent1.agent_id
                agent2_id = agent2.agent_id
                # Set the matrix when the rows point on the current agent choice and the row for the neighbor choice
                agent1.set_neighbors(agent2.agent_id, matrix)
                agent2.set_neighbors(agent1.agent_id, matrix.transpose())   # Set the transpose matrix for the rule up
                # Each agent sent his base random choice for the first iteration threw the communication_network
                agent1.communication_network.send_message(agent2_id, agent1_id, agent2.domain_choice, "base")
                agent2.communication_network.send_message(agent1_id, agent2_id, agent1.domain_choice, "base")


def iteration_total_cost(network):  # Calculate the total cost after for one iteration
    total_network_cost = 0
    visited_agents = set()  # Keep track of visited agent pairs to avoid double counting
    for agent in network:
        agent_cost = 0
        for neighbor_id, neighbor_info in agent.neighbors.items():
            if (neighbor_id, agent.agent_id) not in visited_agents:     # Only not visited neighbors
                neighbor_choice = neighbor_info['base choice']
                matrix = neighbor_info['matrix']
                neighbors_cost = matrix[agent.domain_choice - 1][neighbor_choice - 1]   # The choice combination cost
                agent_cost += neighbors_cost
                visited_agents.add((agent.agent_id, neighbor_id))
        total_network_cost += agent_cost
    return total_network_cost


def dsa_p_correlation():    # Create data frame with the total cost for each p on {rounds}*{runs} changes
    columns = ['p', 'cost']
    df_new = pd.DataFrame(columns=columns)
    for rou in range(rounds):   # Loop over {rounds} different sets of problems
        for p in np.arange(0, 1.05, 0.05):  # Loop over the {p} values of the chance to make choice
            # Set the current agent network - controlled by the seed to create repeat of the same problem between rounds
            random.seed(1+rou)
            communication_network1 = communicationNetwork.Communication_Network()
            network1 = create_agents(communication_network1, n)
            generate_neighbors(network1, k1, cost)
            for r in range(runs):   # Loop over {runs} of set of choices on the same problem
                for run_agent in network1:
                    run_agent.dsa_make_choice(p)    # Each agent make an DSA-C choice
                communication_network1.initialization_iteration("DSA")  # Set the agents state of messages for next run
            # Update the data frame for each p value
            if p in df_new['p'].values:
                df_new.loc[df_new['p'] == p, 'cost'] += iteration_total_cost(network1)
            else:
                df_new_temp = pd.DataFrame({'p': [p], 'cost': [iteration_total_cost(network1)]})
                df_new = pd.concat([df_new, df_new_temp], ignore_index=True)
    return df_new


def algorithms_comparison(neighbor_chance, pro, kind):  # Run DSA-C/MGM with constant parameters - k/p over {Iterations}
    # Define the data to hold the value for each iteration
    new_df_columns = ['Iteration', f'{kind}']
    new_df = pd.DataFrame(columns=new_df_columns)
    # Set the current agent network - controlled by the seed to create repeat of the same problem between rounds
    random.seed(42)
    communication_network2 = communicationNetwork.Communication_Network()
    network2 = create_agents(communication_network2, n)
    generate_neighbors(network2, neighbor_chance, cost)
    # Random start value gets in the data frame
    new_df_temp = pd.DataFrame({'Iteration': [0], f'{kind}': [iteration_total_cost(network2)]})
    new_df = pd.concat([new_df, new_df_temp], ignore_index=True)
    for i in range(iterations):     # Each run try to optimize the problem for {Iterations} times
        for network_agent in network2:
            if kind == "MGM":   # MGM algorithm part 1 - LR calculate
                network_agent.mgm_set_local_reduction()
            else:               # DSA-C algorithm
                network_agent.dsa_make_choice(pro)
        if kind == "MGM":       # MGM algorithm part 2 - choices making
            for network_agent in network2:
                network_agent.mgm_make_choice()
        communication_network2.initialization_iteration(kind)   # Reset indication for new iteration send to all agents
        # Update the current iteration value in the data frame
        new_df_temp = pd.DataFrame({'Iteration': [i], f'{kind}': [iteration_total_cost(network2)]})
        new_df = pd.concat([new_df, new_df_temp], ignore_index=True)
    return new_df


# Graph number 1 - DSA-C for vary of p values
df1 = dsa_p_correlation()
df1['cost'] = df1['cost'] / (runs*rounds)
plt.figure(100)
plt.plot(df1['p'], df1['cost'], marker='o')
plt.xlabel('P')
plt.ylabel('Cost')
plt.title('Graph 1 - Costs vs P')
plt.grid(True)

# Graph number 2 - algorithms comparison for k=0.2 in DSA-C.07, DSA-C.02 and MGM
df2 = algorithms_comparison(k1, p1, "DSA-C : P=O.7")
df2['DSA-C : P=O.2'] = algorithms_comparison(k1, p2, "DSA-C : P=O.2")['DSA-C : P=O.2']
df2['MGM'] = algorithms_comparison(k1, p1, "MGM")['MGM']
plt.figure(200)
plt.plot(df2['Iteration'], df2['DSA-C : P=O.7'], '-', label='DSA-C : P=O.7')
plt.plot(df2['Iteration'], df2['DSA-C : P=O.2'], '-', label='DSA-C : P=O.2')
plt.plot(df2['Iteration'], df2['MGM'], '-', label='MGM')
plt.xlabel('Iteration')
plt.ylabel('Cost')
plt.title('Graph 2 - Iteration vs Cost')
plt.legend()
plt.grid(True)

# Graph number 3 - algorithms comparison for k=0.7 in DSA-C.07, DSA-C.02 and MGM
df3 = algorithms_comparison(k2, p1, "DSA-C : P=O.7")
df3['DSA-C : P=O.2'] = algorithms_comparison(k2, p2, "DSA-C : P=O.2")['DSA-C : P=O.2']
df3['MGM'] = algorithms_comparison(k2, p1, "MGM")['MGM']
plt.figure(300)
plt.plot(df3['Iteration'], df3['DSA-C : P=O.7'], '-', label='DSA-C : P=O.7')
plt.plot(df3['Iteration'], df3['DSA-C : P=O.2'], '-', label='DSA-C : P=O.2')
plt.plot(df2['Iteration'], df2['MGM'], '-', label='MGM')
plt.xlabel('Iteration')
plt.ylabel('Cost')
plt.title('Graph 3 - Iteration vs Cost')
plt.legend()
plt.grid(True)
plt.show()
