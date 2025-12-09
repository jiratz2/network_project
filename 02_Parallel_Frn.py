def distribute_to_buckets(data, n_buckets, data_range=100):
    """แจกจ่ายข้อมูลไปยัง Buckets ตามช่วงค่า."""
    print("--- 1. การแจกจ่าย (Distribute) ---")
    buckets = [[] for _ in range(n_buckets)]
    range_per_bucket = data_range // n_buckets
    
    for item in data:

        if item == data_range:
            bucket_index = n_buckets - 1
        else:
            bucket_index = item // range_per_bucket
        
        bucket_index = min(bucket_index, n_buckets - 1)
        
        buckets[bucket_index].append(item)
    
    for i, bucket in enumerate(buckets):
        print(f"Bucket {i}: {bucket}")
        
    return buckets

def parallel_sort_buckets(buckets):
    """จำลองการจัดเรียงแบบขนาน (แต่ละ Bucket ถูกจัดเรียงโดย Processor)"""
    print("\n--- 2. การจัดเรียงแบบขนาน (Parallel Sort) ---")
    sorted_results = {}
    
    for i, bucket in enumerate(buckets):
        bucket.sort()
        processor_name = f'P{i+1}'
        sorted_results[processor_name] = bucket
        print(f"Processor {processor_name} จัดเรียง Bucket {i}: {bucket}")
        
    return sorted_results

def combine_results(sorted_buckets_map):
    """รวมผลลัพธ์จาก Buckets ที่จัดเรียงแล้ว"""
    print("\n--- 3. การรวมผลลัพธ์ (Combine) ---")
    final_sorted_list = []
   
    for i in range(len(sorted_buckets_map)):
        key = f'P{i+1}'
        final_sorted_list.extend(sorted_buckets_map[key])
        
    return final_sorted_list

input_data = [78, 23, 45, 12, 99, 56, 34, 8, 67, 10, 50, 91]
NUM_BUCKETS = 4

print("### Parallel Sorting (Bucketing) Proof of Concept ###")
print(f"ข้อมูลเริ่มต้น: {input_data}\n")

initial_buckets = distribute_to_buckets(input_data, NUM_BUCKETS)

sorted_data_by_processor = parallel_sort_buckets(initial_buckets)

final_sorted_list = combine_results(sorted_data_by_processor)

print(f"\n# ผลลัพธ์สุดท้าย: {final_sorted_list}")