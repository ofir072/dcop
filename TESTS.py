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

# def agents_data(network):
#     for agent in network:
#         print(f"Agent ID: {agent.agent_id}")
#         print(f"Agent Domain: {agent.domain}")
#         print(f"Agent Choice: {agent.domain_choice}")
#         print(f"Agent LC: {agent.loc_red}")
#         print(f"Agent Next Choice: {agent.next_choice}")
#         for neighbor_id, neighbor_info in agent.neighbors.items():
#             print(f"Neighbor ID: {neighbor_id}")
#             print(f"Neighbor base choice: {neighbor_info['base choice']}")
#             print(f"Neighbor local reduction: {neighbor_info['LR value']}")
#             neighbor_matrix = neighbor_info['matrix']
#             for row in neighbor_matrix:
#                 print(row)
#             print()
#         print("------")
#
#
# communication_network2 = communicationNetwork.Communication_Network()
# network2 = create_agents(communication_network2, n)
# generate_neighbors(network2, k1, cost)
# agents_data(network2)
# for network_agent in network2:
#     network_agent.mgm_set_local_reduction()
# agents_data(network2)
# for network_agent in network2:
#     network_agent.mgm_make_choice()
# communication_network2.initialization_iteration("MGM")
# agents_data(network2)
