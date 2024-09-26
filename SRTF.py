def SRTF(queue):
    # Sort processes 
    queue = sorted(queue, key=lambda x: x["arrival"])
    
    time = 0  
    res = []  
    n = len(queue)  # Total processes
    complete = 0  # Number processes completed
    remaining_time = {proc['id']: proc['execution'] for proc in queue}  # Remaining execution time of each process
    last_proc_id = None  # Track current process
    completion_time = {}  # Track completion time of each process
    
    while complete != n:
        # Find the process with the shortest remaining time that has already arrived
        current_proc = None
        for proc in queue:
            if proc['arrival'] <= time and remaining_time[proc['id']] > 0:
                if current_proc is None or remaining_time[proc['id']] < remaining_time[current_proc['id']]:
                    current_proc = proc
        
        if current_proc is None:
            # If no process has arrived increment time
            time += 1
            continue
        
        # Track process execution in result
        if last_proc_id != current_proc['id']:
            res.append({"time": time, "proc_id": current_proc['id']})
        
        # Reduce the remaining time of the current process
        remaining_time[current_proc['id']] -= 1
        last_proc_id = current_proc['id']
        
        # If process is completed
        if remaining_time[current_proc['id']] == 0:
            complete += 1
            completion_time[current_proc['id']] = time + 1  # Process completes at time + 1 (because of 0-based index)
        
        # Increment the time
        time += 1
    
    # TET
    total_execution_time = max(completion_time.values())
    
    # TAT and WT
    total_turnaround_time = 0
    total_waiting_time = 0
    for proc in queue:
        tat = completion_time[proc['id']] - proc['arrival']  # Turnaround time
        wt = tat - proc['execution']  # Waiting time
        total_turnaround_time += tat
        total_waiting_time += wt
    
    # ATT and AWT
    average_turnaround_time = total_turnaround_time / n
    average_waiting_time = total_waiting_time / n
    
    return {
        "execution_order": res,
        "average_waiting_time": average_waiting_time,
        "average_turnaround_time": average_turnaround_time,
        "total_execution_time": total_execution_time
    }

# proc = [
#     {"id": 0, "arrival": 0, "execution": 7},
#     {"id": 1, "arrival": 2, "execution": 4},
#     {"id": 2, "arrival": 4, "execution": 1},
#     {"id": 3, "arrival": 5, "execution": 4}
# ]

# result = SRTF(proc)
# print("Execution Order:", result["execution_order"])
# print("Average Waiting Time:", result["average_waiting_time"])
# print("Average Turnaround Time:", result["average_turnaround_time"])
# print("Total Execution Time:", result["total_execution_time"])
