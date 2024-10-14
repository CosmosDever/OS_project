def multilevel_feedback(proc, quantum):
    n = len(proc)
    t = 0  
    completed = []  
    process_order = []  
    waiting_times = [0] * n  
    turnaround_times = [0] * n  

    queue_0 = []  
    queue_1 = []  

    proc = sorted(proc, key=lambda x: x["arrival"])
    
    queue_0.append(proc[0])
    proc_idx = 1  

    while queue_0 or queue_1 or proc_idx < n:
        while proc_idx < n and proc[proc_idx]["arrival"] <= t:
            queue_0.append(proc[proc_idx])
            proc_idx += 1

        if queue_0:
            p = queue_0.pop(0)  
            if t < p["arrival"]:
                t = p["arrival"]  

            process_order.append({"time": t, "proc_id": p["id"]})

            exec_time = min(p["execution"], quantum)
            t += exec_time
            p["execution"] -= exec_time

            if p["execution"] > 0:
                queue_1.append(p)
            else:
                turnaround_times[p["id"]] = t - p["arrival"]
                completed.append(p)

        elif queue_1:
            p = queue_1.pop(0) 
            if t < p["arrival"]:
                t = p["arrival"]  

            process_order.append({"time": t, "proc_id": p["id"]})

            t += p["execution"]
            turnaround_times[p["id"]] = t - p["arrival"]
            completed.append(p)

        for i, p in enumerate(proc):
            if p["execution"] > 0:  
                waiting_times[p["id"]] = turnaround_times[p["id"]] - (p["execution"] + exec_time)

    average_waiting_time = sum(waiting_times) / n
    average_turnaround_time = sum(turnaround_times) / n

    result = {
        "execution_order": process_order,
        "average_waiting_time": average_waiting_time,
        "average_turnaround_time": average_turnaround_time,
        "total_execution_time": t
    }

    return result

# proc = [
#     {"id": 0, "arrival": 1, "execution": 3},
#     {"id": 1, "arrival": 3, "execution": 6},
#     {"id": 2, "arrival": 5, "execution": 8},
#     {"id": 3, "arrival": 7, "execution": 4},
#     {"id": 4, "arrival": 8, "execution": 5}
# ]
# quantum = 2
# result = multilevel_feedback(proc, quantum)

# print("Execution Order:", result["execution_order"])
# print("Average Waiting Time:", result["average_waiting_time"])
# print("Average Turnaround Time:", result["average_turnaround_time"])
# print("Total Execution Time:", result["total_execution_time"])

