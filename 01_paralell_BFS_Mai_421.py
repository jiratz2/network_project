import threading
import queue
import time

#Cities and Distances
cities = ["Bangkok", "Chiang Mai", "Phuket", "Khon Kaen"]

dist = {
    ("Bangkok", "Chiang Mai"): 700,
    ("Bangkok", "Phuket"): 840,
    ("Bangkok", "Khon Kaen"): 450,
    ("Chiang Mai", "Phuket"): 1200,
    ("Chiang Mai", "Khon Kaen"): 600,
    ("Phuket", "Khon Kaen"): 1100
}

def get_distance(a, b):
    return dist.get((a, b)) or dist.get((b, a)) or 9999

# Shared Data for BFS
path_queue = queue.Queue()
best_path = None
best_distance = float('inf')
lock = threading.Lock()

# start at Bangkok
path_queue.put(["Bangkok"])

# Worker Logic
def bfs_worker(name):
    global best_path, best_distance

    while True:
        try:
            current_path = path_queue.get(timeout=1)
        except queue.Empty:
            break  # No more tasks
        
        last = current_path[-1]

        #thread ไหนกำลัง process อะไร
        print(f"[{name}] Expanding: {' -> '.join(current_path)}\n")
        time.sleep(0.1)  # ช้าเล็กน้อยเพื่อดู parallel log

        # If visited all cities = close loop
        if len(current_path) == len(cities):
            complete_path = current_path + ["Bangkok"]
            total = 0

            # Calculate total distance
            for i in range(len(complete_path) - 1):
                total += get_distance(complete_path[i], complete_path[i+1])

            # Update best
            with lock:
                if total < best_distance:
                    best_distance = total
                    best_path = complete_path
                    print(f"\n!![{name}] NEW BEST FOUND: {best_path} = {total} km!!\n")

            path_queue.task_done()
            continue

        # Otherwise expand BFS
        for c in cities:
            if c not in current_path:
                new_path = current_path + [c]
                path_queue.put(new_path)

        path_queue.task_done()


#Run Program
threads = []
for i in range(3):
    t = threading.Thread(target=bfs_worker, args=(f"Worker-{i+1}",))
    t.start()
    threads.append(t)
for t in threads:
    t.join()

print("\n========== RESULT ==========")
print("Best Route:", " -> ".join(best_path))
print("Total Distance:", best_distance, "km")
print("============================")
