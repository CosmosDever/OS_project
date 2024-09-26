import random

def generate_process_data(num_processes):

    processes = []
    for i in range(5,num_processes):
        process = {
            "id": i, 
            "arrival": random.randint(0, num_processes*2),  
            "execution": random.randint(1, num_processes*2)  
        }
        processes.append(process)
    
    return processes

# num_processes = 20
# process_data = generate_process_data(num_processes)
# print(process_data)
