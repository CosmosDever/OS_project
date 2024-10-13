def RR(proc, quantum):
    n = len(proc)
    t = 0  # เวลาปัจจุบัน
    completed = [] #ct
    waiting_times = [0] * n #wt
    turnaround_times = [0] * n #tat
    remaining_times = [p["execution"] for p in proc]
    total_execution_time = 0
    queue = []  # คิวของ process ที่พร้อมประมวลผล
    process_order = []

    # เริ่มต้นใส่ process ที่มาถึงแล้ว
    queue.append(proc[0]["id"])

    # ทำงานจนกว่าทุก process จะเสร็จสมบูรณ์
    while queue or any(rt > 0 for rt in remaining_times):
        if queue:
            current_id = queue.pop(0)  # หยิบ process ที่อยู่หน้าสุดในคิว
            current_proc = next(p for p in proc if p["id"] == current_id)
            idx = current_proc["id"]

            # ถ้ากระบวนการยังไม่เสร็จ
            if remaining_times[idx] > 0:
                # บันทึก process ที่กำลังทำงาน พร้อมกับเวลาที่เริ่มทำงาน
                process_order.append({"time" : t,"proc_id" : current_proc["id"]})

                # ประมวลผลกระบวนการตาม quantum
                if remaining_times[idx] > quantum:
                    t += quantum
                    remaining_times[idx] -= quantum
                else:
                    t += remaining_times[idx]
                    remaining_times[idx] = 0
                    completed.append(current_proc)

                    # คำนวณ Turnaround Time และ Waiting Time
                    turnaround_times[idx] = t - current_proc["arrival"]
                    waiting_times[idx] = turnaround_times[idx] - current_proc["execution"]

            # ตรวจสอบว่ามี process อื่นที่มาถึงในระหว่างนั้นหรือไม่ และใส่เข้าไปในคิว
            for p in proc:
                if p["arrival"] <= t and p["id"] not in queue and p["id"] != current_id and remaining_times[p["id"]] > 0:
                    queue.append(p["id"])

            # ถ้า process ยังไม่เสร็จให้ใส่กลับเข้าคิว
            if remaining_times[idx] > 0:
                queue.append(current_id)
            else:
                t += 1

    # คำนวณค่าเฉลี่ยของ Waiting Time และ Turnaround Time
    average_waiting_time = sum(waiting_times) / n
    average_turnaround_time = sum(turnaround_times) / n
    total_execution_time = t

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

quantum = 2  # ตั้ง time quantum

result = RR(proc, quantum)

print("Execution Order:",result["execution_order"])
print("Average Waiting Time:", result["average_waiting_time"])
print("Average Turnaround Time:", result["average_turnaround_time"])
print("Total Execution Time:", result["total_execution_time"])
