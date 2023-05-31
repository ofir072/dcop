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
        communication_network.network.append(new_agent)
    return all_agents


def generate_neighbors(network, probability, upper_cost):    # Generate neighbors in the network
    for i in range(len(network)):
        for j in range(i + 1, len(network)):    # Loop other the remaining pairs for the upcoming agent
            if random.random() < probability:   # Probability of neighbors filter
                matrix = np.array([[random.randint(0, upper_cost) for _ in range(domain)] for _ in range(domain)])
                agent1 = network[i]
                agent2 = network[j]
                agent1_id = agent1.agent_id
                agent2_id = agent2.agent_id
                agent1.set_neighbors(agent2.agent_id, matrix)
                agent2.set_neighbors(agent1.agent_id, matrix.transpose())
                agent1.communication_network.send_message(agent2_id, agent1_id, agent2.domain_choice, "base")
                agent2.communication_network.send_message(agent1_id, agent2_id, agent1.domain_choice, "base")


def initialization_iteration(network):
    for network_agent in network:
        network_agent.update_next_iteration_choices()


def agents_data(network):
    for agent in network:
        print(f"Agent ID: {agent.agent_id}")
        print(f"Agent Domain: {agent.domain}")
        print(f"Agent Choice: {agent.domain_choice}")
        for neighbor_id, neighbor_info in agent.neighbors.items():
            print(f"Neighbor ID: {neighbor_id}")
            print(f"Neighbor base choice: {neighbor_info['base choice']}")
            print(f"Neighbor next choice: {neighbor_info['next choice']}")
            neighbor_matrix = neighbor_info['matrix']
            for row in neighbor_matrix:
                print(row)
            print()
        print("------")


def iteration_total_cost(network):
    total_network_cost = 0
    visited_agents = set()  # Keep track of visited agent pairs to avoid double counting
    for agent in network:
        agent_cost = 0
        for neighbor_id, neighbor_info in agent.neighbors.items():
            if (neighbor_id, agent.agent_id) not in visited_agents:
                neighbor_choice = neighbor_info['base choice']
                matrix = neighbor_info['matrix']
                neighbors_cost = matrix[agent.domain_choice - 1][neighbor_choice - 1]
                agent_cost += neighbors_cost
                visited_agents.add((agent.agent_id, neighbor_id))
        total_network_cost += agent_cost
    return total_network_cost


def dsa_p_correlation():
    columns = ['p', 'cost']
    df_new = pd.DataFrame(columns=columns)
    for rou in range(rounds):
        # print(f"Round: {rou}")
        for p in np.arange(0, 1.05, 0.05):
            # print(f"p: {p}")
            random.seed(1+rou)
            communication_network1 = communicationNetwork.Communication_Network()
            network1 = create_agents(communication_network1, n)
            generate_neighbors(network1, k1, cost)
            for r in range(runs):
                # print(f"Run: {r}")
                for run_agent in network1:
                    run_agent.dsa_make_choice(p)
                initialization_iteration(network1)
            if p in df_new['p'].values:
                df_new.loc[df_new['p'] == p, 'cost'] += iteration_total_cost(network1)
            else:
                df_new_temp = pd.DataFrame({'p': [p], 'cost': [iteration_total_cost(network1)]})
                df_new = pd.concat([df_new, df_new_temp], ignore_index=True)
    return df_new


def algorithms_comparison(neighbor_chance, pro, kind):
    new_df_columns = ['Iteration', f'{kind}']
    new_df = pd.DataFrame(columns=new_df_columns)
    random.seed(42)
    communication_network2 = communicationNetwork.Communication_Network()
    network2 = create_agents(communication_network2, n)
    generate_neighbors(network2, neighbor_chance, cost)
    for i in range(iterations):
        for network_agent in network2:
            network_agent.dsa_make_choice(pro)
        initialization_iteration(network2)
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
plt.figure(200)
plt.plot(df2['Iteration'], df2['DSA-C : P=O.7'], '-', label='Graph 2: DSA-C : P=O.7')
plt.plot(df2['Iteration'], df2['DSA-C : P=O.2'], '-', label='Graph 2: DSA-C : P=O.2')
plt.xlabel('Iteration')
plt.ylabel('Cost')
plt.title('Graph 2 - Iteration vs Cost')
plt.legend()
plt.grid(True)

# Graph number 3 - algorithms comparison for k=0.7 in DSA-C.07, DSA-C.02 and MGM
df3 = algorithms_comparison(k2, p1, "DSA-C : P=O.7")
df3['DSA-C : P=O.2'] = algorithms_comparison(k2, p2, "DSA-C : P=O.2")['DSA-C : P=O.2']
plt.figure(300)
plt.plot(df3['Iteration'], df3['DSA-C : P=O.7'], '-', label='Graph 3: DSA-C : P=O.7')
plt.plot(df3['Iteration'], df3['DSA-C : P=O.2'], '-', label='Graph 3: DSA-C : P=O.2')
plt.xlabel('Iteration')
plt.ylabel('Cost')
plt.title('Graph 3 - Iteration vs Cost')
plt.legend()
plt.grid(True)
plt.show()

# # Combined plot
# plt.figure(400)
# plt.plot(df2['Iteration'], df2['DSA-C : P=O.7'], '-', label='Graph 2: DSA-C : P=O.7')
# plt.plot(df2['Iteration'], df2['DSA-C : P=O.2'], '-', label='Graph 2: DSA-C : P=O.2')
# plt.plot(df3['Iteration'], df3['DSA-C : P=O.7'], '-', label='Graph 3: DSA-C : P=O.7')
# plt.plot(df3['Iteration'], df3['DSA-C : P=O.2'], '-', label='Graph 3: DSA-C : P=O.2')
# plt.xlabel('Iteration')
# plt.ylabel('Cost')
# plt.title('Combined Graph - Iteration vs Cost')
# plt.legend()
# plt.grid(True)
