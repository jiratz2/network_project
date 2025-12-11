import hashlib

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.next = None
        self.storage = {}

    def set_next(self, node):
        self.next = node

    # แฮชให้กลายเป็นตัวเลข 0-100
    def hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16) % 100

    # Upload (store)
    def upload(self, filename):
        h = self.hash(filename)
        print(f"\n[UPLOAD] Start uploading '{filename}' (hash={h}) at Node {self.id}")
        self._store(h, filename)

    def _store(self, h, filename):
        # Node นี้รับผิดชอบไหม? (id >= hash) หรือเกิด wrap
        if self.id >= h or (self.next.id < self.id and h > self.id):
            self.storage[filename] = f"[DATA of {filename}]"
            print(f"   => Stored at Node {self.id}")
        else:
            print(f"   => Node {self.id} passing to Node {self.next.id}")
            self.next._store(h, filename)

    # Download
    def download(self, filename):
        print(f"\n[DOWNLOAD] Searching '{filename}' starting at Node {self.id}")
        return self._lookup(filename)

    def _lookup(self, filename):
        if filename in self.storage:
            print(f"   => FOUND at Node {self.id}")
            return self.storage[filename]
        else:
            print(f"   => Not here at Node {self.id}, try Node {self.next.id}")
            return self.next._lookup(filename)


# Simulation
n1 = Node(10)
n2 = Node(40)
n3 = Node(70)
n4 = Node(90)

# Create ring
n1.set_next(n2)
n2.set_next(n3)
n3.set_next(n4)
n4.set_next(n1)

print("Torrent-DHT Ring Structure:")
print("Ring:", "10 > 40 > 70 > 90 > 10")

# Upload files
n1.upload("Avengers_Endgame.mkv")
n1.upload("Ubuntu_22.04.iso")
n1.upload("Assignment_Final.docx")

# Download example
n1.download("Ubuntu_22.04.iso")
n1.download("Avengers_Endgame.mkv")
