import copy

INF = 999

class Node:
    def __init__(self, node_id, all_nodes):
        self.id = node_id
        self.dv = {n: (0 if n == node_id else INF) for n in all_nodes}
        self.neighbors = {} 

    def add_neighbor(self, neighbor_id, cost):
        self.neighbors[neighbor_id] = cost

    def receive_update(self, neighbor_id, neighbor_dv):
        updated = False
        cost_to_neighbor = self.neighbors[neighbor_id]

        print(f"   [Node {self.id}] Received DV from Node {neighbor_id} (Cost to neighbor: {cost_to_neighbor})")

        for dest_node, dist_from_neighbor in neighbor_dv.items():
            new_dist = cost_to_neighbor + dist_from_neighbor
            
            if new_dist < self.dv[dest_node]:
                print(f"     Update Route to Node {dest_node}: {self.dv[dest_node]} -> {new_dist}")
                self.dv[dest_node] = new_dist
                updated = True
        
        return updated

def run_simulation():
    node_names = ['A', 'B', 'C', 'D']
    nodes = {name: Node(name, node_names) for name in node_names}
    edges = [
        ('A', 'B', 1),
        ('B', 'C', 2),
        ('C', 'D', 1),
        ('A', 'D', 5) 
    ]

    for u, v, w in edges:
        nodes[u].add_neighbor(v, w)
        nodes[v].add_neighbor(u, w)

    print("--- Initial State ---")
    for n in nodes.values():
        print(f"Node {n.id} DV: {n.dv}")
    print("-" * 30)
    converged = False
    round_count = 1

    while not converged:
        print(f"\n>>> Round {round_count}")
        converged = True 
        
        current_dvs = {name: copy.deepcopy(node.dv) for name, node in nodes.items()}

        for name, node in nodes.items():
            for neighbor_id in node.neighbors:
                neighbor_vector = current_dvs[neighbor_id]
                is_changed = node.receive_update(neighbor_id, neighbor_vector)
                
                if is_changed:
                    converged = False 

        round_count += 1
        
        print("\n--- Current Routing Tables ---")
        for n in nodes.values():
            print(f"Node {n.id}: {n.dv}")
        
        if round_count > len(node_names) + 2: 
            print("Force Stop (Count exceeded)")
            break

    print("Final Result (Shortest Path from A to D [A->B->C->D]):")
    print(f"Node A thinks dist to D is: {nodes['A'].dv['D']}")

if __name__ == "__main__":
    run_simulation()