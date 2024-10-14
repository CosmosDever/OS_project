<<<<<<< Updated upstream
from collections import deque

class Process:
    def __init__(self, pid, arrival_time, execution_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.start_time = -1

def mlfq_scheduler(processes, time_quantums):
    queues = [deque(), deque(), deque()]
    time = 0  
    completed_processes = []
    ready_processes = deque()  

    processes.sort(key=lambda p: p.arrival_time)

    q1_time_quantum, q2_time_quantum, q3_time_quantum = time_quantums

    while processes or any(queues) or ready_processes:
        while processes and processes[0].arrival_time <= time:
            ready_processes.append(processes.pop(0))
        
        while ready_processes:
            queues[0].append(ready_processes.popleft())

        for i, queue in enumerate(queues):
            if queue:
                current_process = queue.popleft()

                if current_process.start_time == -1:
                    current_process.start_time = time

                if i == 0:
                    time_quantum = q1_time_quantum
                elif i == 1:
                    time_quantum = q2_time_quantum
                else:
                    time_quantum = q3_time_quantum

                execution_time = min(time_quantum, current_process.remaining_time)
                time += execution_time
                current_process.remaining_time -= execution_time

                if current_process.remaining_time == 0:
                    current_process.turnaround_time = time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.execution_time
                    completed_processes.append(current_process)
                else:
                    if i < 2:
                        queues[i + 1].append(current_process)
                    else:
                        queues[i].append(current_process)
                break
        else:
            time += 1

    return completed_processes

process_list = [
    {"id": 0, "arrival": 0, "execution": 9},
    {"id": 1, "arrival": 1, "execution": 6},
    {"id": 2, "arrival": 2, "execution": 2},
    {"id": 3, "arrival": 3, "execution": 4},
]

processes = [Process(p["id"], p["arrival"], p["execution"]) for p in process_list]

time_quantums = [4, 6, 8]  

completed = mlfq_scheduler(processes, time_quantums)

for process in completed:
    print(f"Process {process.pid}: Start Time = {process.start_time}, "
          f"Turnaround Time = {process.turnaround_time}, Waiting Time = {process.waiting_time}")
=======
def multilevel_feedback(proc):
    n = len(proc)
    t = 0  
    quantum = 4  
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

proc = [
    {"id": 0, "arrival": 1, "execution": 3},
    {"id": 1, "arrival": 3, "execution": 6},
    {"id": 2, "arrival": 5, "execution": 8},
    {"id": 3, "arrival": 7, "execution": 4},
    {"id": 4, "arrival": 8, "execution": 5}
]

result = multilevel_feedback(proc)

print("Execution Order:", result["execution_order"])
print("Average Waiting Time:", result["average_waiting_time"])
print("Average Turnaround Time:", result["average_turnaround_time"])
print("Total Execution Time:", result["total_execution_time"])
>>>>>>> Stashed changes
