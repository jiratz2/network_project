from multiprocessing import Pool
import random

def sort_bucket(bucket):
    """ให้ process ลูก sort bucket"""
    return sorted(bucket)

if __name__ == "__main__":
    print("=== Parallel Bucket Sorting ===")

    # สร้างข้อมูลสุ่ม
    data = [random.randint(0, 1000) for _ in range(50)]
    print("Input:", data)

    num_buckets = 4
    max_value = max(data)
    bucket_range = max_value // num_buckets + 1

    # สร้าง bucket ว่าง
    buckets = [[] for _ in range(num_buckets)]

    # กระจายข้อมูลลง bucket
    for value in data:
        index = value // bucket_range
        buckets[index].append(value)

    # ใช้ multiprocess sort
    pool = Pool(processes=num_buckets)
    sorted_buckets = pool.map(sort_bucket, buckets)

    # รวมกลับเป็นอาเรย์สุดท้าย
    result = []
    for b in sorted_buckets:
        result.extend(b)

    print("Sorted:", result)
