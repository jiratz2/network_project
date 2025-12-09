import hashlib

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.storage = {} # เก็บไฟล์ใน Dictionary {filename: content}

    def __repr__(self):
        return f"[Node ID: {self.id} | Files: {list(self.storage.keys())}]"

class DHT:
    def __init__(self, m_bit_space=5):
        # พื้นที่ ID Space ขนาด 2^m (เช่น m=5 คือ 0-31)
        self.space_size = 2**m_bit_space
        self.nodes = [] # List ของ Node ในวงแหวน

    def add_node(self, node):
        self.nodes.append(node)
        # เรียงลำดับ Node ตาม ID เพื่อจำลองโครงสร้างวงกลม (Ring)
        self.nodes.sort(key=lambda x: x.id)
        print(f"Server added: Node {node.id}")

    def get_hash(self, key):
        # ใช้ SHA1 แล้ว Modulo เพื่อให้ได้เลขในช่วง Space size
        sha1 = hashlib.sha1(key.encode()).hexdigest()
        val = int(sha1, 16)
        return val % self.space_size

    def find_successor(self, key_hash):
        """
        หัวใจสำคัญ: หา Node ตัวแรกที่มี ID >= key_hash
        ถ้าไม่มี (ค่า key สูงกว่า node ตัวสุดท้าย) ให้วนกลับไป Node ตัวแรก (Wrap around)
        """
        for node in self.nodes:
            if node.id >= key_hash:
                return node
        return self.nodes[0] # Wrap around

    def put(self, filename, content):
        key_hash = self.get_hash(filename)
        target_node = self.find_successor(key_hash)
        
        print(f"\n[PUT] Uploading '{filename}'")
        print(f"   -> Hash({filename}) = {key_hash}")
        print(f"   -> Mapped to Successor Node {target_node.id}")
        
        target_node.storage[filename] = content
        print(f"   -> Stored Successfully.")

    def get(self, filename):
        key_hash = self.get_hash(filename)
        target_node = self.find_successor(key_hash)
        
        print(f"\n[GET] Requesting '{filename}'")
        print(f"   -> Hash({filename}) = {key_hash}")
        print(f"   -> Routing request to Node {target_node.id}")
        
        if filename in target_node.storage:
            print(f"   -> FOUND! Content: {target_node.storage[filename]}")
        else:
            print("   -> 404 Not Found.")

    def print_ring_status(self):
        print("\n" + "="*30)
        print("DHT NETWORK STATUS (Ring)")
        print("="*30)
        for node in self.nodes:
            print(node)
        print("="*30)

# --- Main Simulation ---
if __name__ == "__main__":
    # สร้างระบบ DHT (ID Space 0-31)
    dht = DHT(m_bit_space=5) 

    # 1. สร้าง Servers (Nodes) กระจายๆ กัน
    dht.add_node(Node(2))
    dht.add_node(Node(10))
    dht.add_node(Node(25))
    
    # 2. จำลองการ Upload ไฟล์ (Put)
    # ระบบจะคำนวณ Hash และโยนไป Node ที่เหมาะสมเอง
    dht.put("movie.mp4", "Video Data 1GB")
    dht.put("report.pdf", "Final Project PDF")
    dht.put("image.png", "Picture Data")
    dht.put("avatar.jpg", "Profile Pic")

    # 3. ดูสถานะว่าไฟล์ไปตกที่ใคร
    dht.print_ring_status()

    # 4. จำลองการ Download (Get)
    # User ไม่ต้องรู้ว่าไฟล์อยู่ที่ไหน แค่ขอชื่อไฟล์ ระบบจะ Hash ไปหา Node นั้นให้
    dht.get("movie.mp4")
    dht.get("unknown.txt") # ลองหาไฟล์ที่ไม่มี