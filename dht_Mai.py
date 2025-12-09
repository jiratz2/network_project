import hashlib

# จำลอง nodes
nodes = {
    "Node-1": {},
    "Node-2": {},
    "Node-3": {}
}

node_list = list(nodes.keys())

# เลือก node จาก hash
def pick_node(key):
    h = int(hashlib.sha1(key.encode()).hexdigest(), 16)
    idx = h % len(node_list)
    return node_list[idx]

# ใส่ข้อมูลลง DHT
def put(key, value):
    node = pick_node(key)
    nodes[node][key] = value
    print(f"[PUT] {key}:{value} -> stored at {node}")

# ดึงข้อมูลจาก DHT
def get(key):
    node = pick_node(key)
    value = nodes[node].get(key, None)
    print(f"[GET] {key} -> lookup at {node} -> result = {value}")
    return value

if __name__ == "__main__":
    # กระจายข้อมูลทดสอบ
    put("apple", 10)
    put("banana", 20)
    put("cat", 30)
    put("dog", 40)
    put("elephant", 50)
    
    print("\n--- Node Storage State ---")
    for n, store in nodes.items():
        print(n, ":", store)
    print("\n--- Lookup Test ---")
    get("banana")
    get("dog")
    get("fish")  # คีย์ที่ไม่มีใน DHT