from multiprocessing import Pool
from itertools import permutations

# --- ตัวอย่างข้อมูลระยะทางระหว่างเมือง ---
# เมือง: A=0, B=1, C=2, D=3
dist_matrix = [
    [0, 4, 1, 9],
    [4, 0, 6, 3],
    [1, 6, 0, 2],
    [9, 3, 2, 0]
]

cities = [0, 1, 2, 3]


def path_cost(path):
    """คำนวณต้นทุนการเดินเส้นทาง"""
    cost = 0
    for i in range(len(path) - 1):
        cost += dist_matrix[path[i]][path[i + 1]]
    cost += dist_matrix[path[-1]][path[0]]  # วนกลับต้นทาง
    return cost


def evaluate_paths(path_batch):
    """ฟังก์ชันให้ process ลูกใช้คำนวณต้นทุนเส้นทาง"""
    results = []
    for p in path_batch:
        results.append((p, path_cost(p)))
    return results


if __name__ == "__main__":
    print("=== Parallel Breadth First Search ===")

    # BFS-Style: ใช้ permutation (แค่ตัวอย่างง่าย)
    all_paths = list(permutations(cities))

    # แบ่งงานเป็นก้อน ๆ
    batch_size = 4
    batches = [all_paths[i:i+batch_size] for i in range(0, len(all_paths), batch_size)]

    pool = Pool(processes=4)
    results = pool.map(evaluate_paths, batches)

    # รวมผล
    flat_result = [item for sublist in results for item in sublist]

    # หาเส้นทางที่ดีที่สุด
    best_path, best_cost = min(flat_result, key=lambda x: x[1])

    print("Best Path:", best_path)
    print("Cost:", best_cost)
