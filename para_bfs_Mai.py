from multiprocessing import Pool, cpu_count

# ตัวอย่างกราฟจำลอง
graph = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'C', 'E'],
    'C': ['A', 'B', 'F'],
    'D': ['A', 'E'],
    'E': ['B', 'D', 'F'],
    'F': ['C', 'E']
}

# ฟังก์ชันขยาย node ใช้โดยแต่ละ worker
def expand_node(node):
    print(f"[Worker] expanding node: {node}")
    return graph.get(node, [])

def parallel_bfs(start, max_depth=3):
    frontier = [start]
    visited = set([start])
    depth = 0

    print(f"Start BFS at node = {start}\n")

    while depth < max_depth:
        print(f"--- Depth {depth} ---")
        print("Frontier:", frontier)

        # ทำ parallel expand
        with Pool(cpu_count()) as pool:
            results = pool.map(expand_node, frontier)

        # รวมอาเรย์ผลลัพธ์
        next_frontier = []
        for neighbors in results:
            for n in neighbors:
                if n not in visited:
                    visited.add(n)
                    next_frontier.append(n)
                    
        print("Expanded to:", next_frontier, "\n")
        frontier = next_frontier
        depth += 1

    print("\nFinal visited:", visited)
    return visited

if __name__ == "__main__":
    parallel_bfs("A")  # เริ่มต้น BFS ที่ node 'A'
