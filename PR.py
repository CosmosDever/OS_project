def priority_scheduling(queue):
    # Sort processes based on arrival time and priority
    queue = sorted(queue, key=lambda x: (x["arrival"], x["priority"]))
    
    time = 0  
    res = []   
    n = len(queue)   # Total processes
    completed = 0  # Number completed processes
    waiting_time = {proc['id']: 0 for proc in queue}  # Track waiting time of each process
    last_proc_id = None  # Track current process
    completed_processes = set()  # Keep track completed processes
    completion_time = {}  # Completion times for each process

    while completed != n:
        candidates = []
        for proc in queue:
            if proc['id'] not in completed_processes and proc['arrival'] <= time:
                candidates.append(proc)

        if not candidates:
            time += 1
            continue

        selected_proc = min(candidates, key=lambda x: (x['priority'], x['arrival']))

        if last_proc_id != selected_proc['id']:
            res.append({"time": time, "proc_id": selected_proc['id']})

        time += selected_proc['execution']
        completion_time[selected_proc['id']] = time

        completed += 1
        completed_processes.add(selected_proc['id'])
        last_proc_id = selected_proc['id']

    total_execution_time = max(completion_time.values())

    total_turnaround_time = 0
    total_waiting_time = 0
    for proc in queue:
        tat = completion_time[proc['id']] - proc['arrival']  
        wt = tat - proc['execution']
        total_turnaround_time += tat
        total_waiting_time += wt

    average_turnaround_time = total_turnaround_time / n
    average_waiting_time = total_waiting_time / n

    return {
        "execution_order": res,
        "average_waiting_time": average_waiting_time,
        "average_turnaround_time": average_turnaround_time,
        "total_execution_time": total_execution_time
    }

proc = [
    {"id": 0, "arrival": 1, "execution": 3, "priority": 2},
    {"id": 1, "arrival": 3, "execution": 6, "priority": 1},
    {"id": 2, "arrival": 5, "execution": 8, "priority": 3},
    {"id": 3, "arrival": 7, "execution": 4, "priority": 2},
    {"id": 4, "arrival": 8, "execution": 5, "priority": 1}
]

result = priority_scheduling(proc)
print("Execution Order:", result["execution_order"])
print("Average Waiting Time:", result["average_waiting_time"])
print("Average Turnaround Time:", result["average_turnaround_time"])
print("Total Execution Time:", result["total_execution_time"])
