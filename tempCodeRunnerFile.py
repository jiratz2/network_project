threads = []
for i in range(3):
    t = threading.Thread(target=bfs_worker, args=(f"Worker-{i+1}",))
    t.start()
    threads.append(t)
for t in threads:
    t.join()