def FCFS(proc):
    n = len(proc)
    t = 0  #เวลาปัจจุบัน
    completed = [] #ct
    waiting_times = [] #wt
    turnaround_times = [] #tat
    total_execution_time = 0
    process_order = []

    
    for p in sorted(proc, key=lambda x: x["arrival"]):  # จัดเรียงตาม arrival time
        # ถ้าเวลาปัจจุบันยังน้อยกว่าการมาถึงของ process ให้เวลาปัจจุบันตรงกับ arrival time
        if t < p["arrival"]:
            t = p["arrival"]

        # บันทึกเวลาที่ process เริ่มทำงานและ ID ของ process
        process_order.append((t, p["id"]))

        
        t += p["execution"]
        total_execution_time += p["execution"]
        turnaround_time = t - p["arrival"]
        waiting_time = turnaround_time - p["execution"]

        completed.append(p)
        turnaround_times.append(turnaround_time)
        waiting_times.append(waiting_time)

    # คำนวณค่าเฉลี่ยของ Waiting Time และ Turnaround Time
    average_waiting_time = sum(waiting_times) / n
    average_turnaround_time = sum(turnaround_times) / n

    result = {
        "execution_order": process_order,
        "average_waiting_time": average_waiting_time,
        "average_turnaround_time": average_turnaround_time,
        "total_execution_time": total_execution_time
    }

    return result

proc = [
    {"id": 0, "arrival": 1, "execution": 3},
    {"id": 1, "arrival": 3, "execution": 6},
    {"id": 2, "arrival": 5, "execution": 8},
    {"id": 3, "arrival": 7, "execution": 4},
    {"id": 4, "arrival": 8, "execution": 5}
]

result = FCFS(proc)

print("Execution Order:", result["execution_order"])
print("Average Waiting Time:", result["average_waiting_time"])
print("Average Turnaround Time:", result["average_turnaround_time"])
print("Total Execution Time:", result["total_execution_time"])