def run_distributed_bellman_ford(nodes, edges, source_node):
    """จำลองการทำงานของ Distributed Bellman-Ford"""
    
    distances = {node: float('inf') for node in nodes}
    distances[source_node] = 0
    
    V = len(nodes)
    
    print(f"### Distributed Bellman-Ford Proof of Concept ###")
    print(f"โหนด: {nodes}, Source: {source_node}")
    print(f"สถานะเริ่มต้น: {distances}")

    for i in range(1, V):
        new_distances = distances.copy()
        
        print(f"\n--- รอบที่ {i} / {V-1} (V-1 Iterations) ---")
        updates_made = False
        
        for u, v, weight in edges:
            if distances[u] != float('inf'):
                
                if distances[u] + weight < new_distances[v]:
                    new_dist_v = distances[u] + weight
                    
                    print(f"  > Node {v} อัปเดต (จาก {u}): {new_distances[v]} -> {new_dist_v}")
                    new_distances[v] = new_dist_v
                    updates_made = True

        distances = new_distances 
        print(f"  สถานะระยะทางหลังรอบที่ {i}: {distances}")

        # ถ้าไม่มีโหนดใดอัปเดตเลย สามารถหยุดการทำงานได้
        #if not updates_made:
        #    print(f"\nไม่มีการอัปเดตในรอบนี้. หยุดการทำงาน.")
        #    break
        
    print("\n--- 4. ตรวจสอบ Negative Cycle ---")
    for u, v, weight in edges:
        if distances[u] != float('inf') and distances[u] + weight < distances[v]:
            print(f"!! ตรวจพบ Negative Cycle: Edge ({u}, {v})")
            return "พบ Negative Cycle"

    return distances

GRAPH_EDGES = [
    ['A', 'B', 6], ['A', 'C', 4],
    ['B', 'D', -3], ['B', 'E', 7],
    ['C', 'B', -2], ['C', 'D', 8],
    ['D', 'E', 5],
]
GRAPH_NODES = ['A', 'B', 'C', 'D', 'E']
START_NODE = 'A'

final_result = run_distributed_bellman_ford(GRAPH_NODES, GRAPH_EDGES, START_NODE)

print(f"\n# ผลลัพธ์สุดท้าย (Shortest Paths from {START_NODE}): {final_result}")