import random

def generate_process_data(num_processes,queue):
    start = max([p["id"] for p in queue]) if queue else -1
    processes = []
    for i in range(num_processes):
        process = {
            "id": i+start+1, 
            "arrival": random.randint(0, num_processes*2),  
            "execution": random.randint(1, num_processes*2),
            "priority" : random.randint(1, num_processes*2)
        }
        processes.append(process)
    
    return processes

# num_processes = 20
# process_data = generate_process_data(num_processes)
# print(process_data)
