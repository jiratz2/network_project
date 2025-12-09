import hashlib

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.storage = {} 
    def __repr__(self):
        return f"[Node ID: {self.id} | Files: {list(self.storage.keys())}]"

class DHT:
    def __init__(self, m_bit_space=5):
        self.space_size = 2**m_bit_space
        self.nodes = [] 

    def add_node(self, node):
        self.nodes.append(node)
        self.nodes.sort(key=lambda x: x.id)
        print(f"Server added: Node {node.id}")

    def get_hash(self, key):
        sha1 = hashlib.sha1(key.encode()).hexdigest()
        val = int(sha1, 16)
        return val % self.space_size

    def find_successor(self, key_hash):
        for node in self.nodes:
            if node.id >= key_hash:
                return node
        return self.nodes[0] 

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

if __name__ == "__main__":
    dht = DHT(m_bit_space=5) 

    dht.add_node(Node(2))
    dht.add_node(Node(10))
    dht.add_node(Node(25))
    
    dht.put("movie.mp4", "Video Data 1GB")
    dht.put("report.pdf", "Final Project PDF")
    dht.put("image.png", "Picture Data")
    dht.put("avatar.jpg", "Profile Pic")

    dht.print_ring_status()

    dht.get("movie.mp4")
    dht.get("unknown.txt")