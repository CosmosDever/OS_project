import tkinter as tk
from tkinter import ttk, messagebox
import HRRN
import SRTF
import SJF
import PR
import FCFS
import MLFQ
import RR
import random_proc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Sample data
process_data = [
    {"id": 0, "arrival": 0, "execution": 7, "priority": 2},
    {"id": 1, "arrival": 2, "execution": 4, "priority": 1},
    {"id": 2, "arrival": 4, "execution": 1, "priority": 3},
    {"id": 3, "arrival": 5, "execution": 4, "priority": 2}
    
]

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Scheduling Simulator")
        self.set_dynamic_geometry()

        # Sample data
        self.process_data = [
            {"id": 0, "arrival": 0, "execution": 7, "priority": 2},
            {"id": 1, "arrival": 2, "execution": 4, "priority": 1},
            {"id": 2, "arrival": 4, "execution": 1, "priority": 3},
            {"id": 3, "arrival": 5, "execution": 4, "priority": 2}
          
        ]

        # Frame for algorithm selection
        self.algorithm_frame = tk.Frame(root)
        self.algorithm_frame.pack(pady=10)

        # Dropdown for selecting algorithm
        self.algorithms = ['HRRN', 'SRTF','SJF','PRIORITY','FCFS','MLFQ','RR']  # Add other algorithms here
        self.selected_algorithm = tk.StringVar()
        self.selected_algorithm.set(self.algorithms[0])

        tk.Label(self.algorithm_frame, text="Select Scheduling Algorithm:").grid(row=0, column=0, padx=5, pady=5)
        self.algo_menu = ttk.Combobox(self.algorithm_frame, values=self.algorithms, textvariable=self.selected_algorithm)
        self.algo_menu.grid(row=0, column=1, padx=5, pady=5)
        
       
        # Button to run the simulation
        self.run_button = tk.Button(self.algorithm_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=0, column=2, padx=5, pady=5)

        #input number of random process
        self.random_process_label = tk.Label(self.algorithm_frame, text="Number of Random Processes")
        self.random_process_label.grid(row=0, column=4, padx=5, pady=5)
        self.random_process_entry = tk.Entry(self.algorithm_frame)
        self.random_process_entry.grid(row=0, column=5, padx=5, pady=5)

        #add random process button
        self.random_process_button = tk.Button(self.algorithm_frame, text="Add Random Process", command=self.add_random_process)
        self.random_process_button.grid(row=0, column=3, padx=5, pady=5)

        # Frame for process input
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10)

        tk.Label(self.input_frame, text="Process ID:").grid(row=0, column=0)
        self.id_entry = tk.Entry(self.input_frame)
        self.id_entry.grid(row=0, column=1)

        tk.Label(self.input_frame, text="Arrival Time:").grid(row=0, column=2)
        self.arrival_entry = tk.Entry(self.input_frame)
        self.arrival_entry.grid(row=0, column=3)

        tk.Label(self.input_frame, text="Execution Time:").grid(row=0, column=4)
        self.execution_entry = tk.Entry(self.input_frame)
        self.execution_entry.grid(row=0, column=5)

        tk.Label(self.input_frame, text="Priority:").grid(row=0, column=6)
        self.priority_entry = tk.Entry(self.input_frame)
        self.priority_entry.grid(row=0, column=7)

        # Button to add a process
        self.add_process_button = tk.Button(self.input_frame, text="Add Process", command=self.add_process)
        self.add_process_button.grid(row=0, column=8, padx=5, pady=5)
        
        # Entry for quantum
        self.quantum_label = tk.Label(self.algorithm_frame, text="Quantum:")
        self.quantum_label.grid(row=0, column=9, padx=5, pady=5)
        self.quantum_entry = tk.Entry(self.algorithm_frame)
        self.quantum_entry.grid(row=0, column=10, padx=5, pady=5)


        # Table for process data
        self.process_frame = tk.Frame(root)
        self.process_frame.pack(pady=5)
        self.create_process_table()

        # Area for displaying the simulation results
        self.result_frame = tk.Frame(root)
        self.result_frame.pack(pady=10)

        self.result_label = tk.Label(self.result_frame, text="Simulation Result", font=('Arial', 16))
        self.result_label.pack(pady=10)

        self.result_text = tk.Text(self.result_frame, height=10, width=80)
        self.result_text.pack()
    
        # Frame for the Gantt chart
        self.chart_frame = tk.Frame(root)
        self.chart_frame.pack(pady=10)
    
    #quantum input
    def get_quantum(self):
        try:
            quantum = int(self.quantum_entry.get())
            return quantum
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer value for quantum.")
            return None
        
        
    def set_dynamic_geometry(self):
        """Set the window size dynamically based on the number of processes."""
        base_width = 1920  # Base width for the window
        base_height = 1080  # Base height for the window
        num_processes = len(process_data)
        
        # Calculate width based on the number of processes
        dynamic_width = base_width + (num_processes * 50)  # Adjust the multiplier as needed
        dynamic_height = base_height + 200  # Adjust height as needed for the Gantt chart

        self.root.geometry(f"{dynamic_width}x{dynamic_height}")    
    
    def add_random_process(self):
        num_processes = int(self.random_process_entry.get())
        process_data = random_proc.generate_process_data(num_processes,self.process_data)
        for proc in process_data:
            self.process_data.append(proc)
        self.update_process_table()
    def create_process_table(self):
        """Create a table that displays the process data."""
        tk.Label(self.process_frame, text="Process Data", font=('Arial', 16)).pack(pady=10)

        columns = ('ID', 'Arrival Time', 'Execution Time', 'Priority')
        self.tree = ttk.Treeview(self.process_frame, columns=columns, show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Arrival Time', text='Arrival Time')
        self.tree.heading('Execution Time', text='Execution Time')
        self.tree.heading('Priority', text='Priority')


        # Insert process data into the table
        for proc in self.process_data:
            self.tree.insert('', tk.END, values=(proc['id'], proc['arrival'], proc['execution'],proc['priority']))
        self.tree.pack(pady=10)

    def add_process(self):
        """Add a new process to the process data and update the table."""
        try:
            proc_id = int(self.id_entry.get())
            arrival = int(self.arrival_entry.get())
            execution = int(self.execution_entry.get())
            priority = int(self.priority_entry.get())

            # Validate inputs
            if any(proc['id'] == proc_id for proc in self.process_data):
                messagebox.showerror("Error", "Process ID must be unique.")
                return

            new_process = {'id': proc_id, 'arrival': arrival, 'execution': execution, 'priority': priority}
            self.process_data.append(new_process)

            # Clear the entries
            self.id_entry.delete(0, tk.END)
            self.arrival_entry.delete(0, tk.END)
            self.execution_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)

            # Update the process table
            self.update_process_table()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer values for ID, Arrival Time, and Execution Time.")

    def update_process_table(self):
        """Update the process table with the current process data."""
        # Clear the existing table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert updated process data into the table
        for proc in self.process_data:
            self.tree.insert('', tk.END, values=(proc['id'], proc['arrival'], proc['execution'],proc['priority']))

    def run_simulation(self):
        """Run the selected scheduling algorithm and display the result."""
        self.result_text.delete(1.0, tk.END)  # Clear previous result

        # Get the selected algorithm
        algorithm = self.selected_algorithm.get()

        # Execute the selected algorithm
        if algorithm == 'HRRN':
            result = HRRN.HRRN(self.process_data)
        elif algorithm == 'SRTF':
            result = SRTF.SRTF(self.process_data)
        elif algorithm == 'SJF':
            result = SJF.sjf_non_preemptive(self.process_data)   
        elif algorithm == 'PRIORITY':
            result = PR.priority_scheduling(self.process_data)
        elif algorithm == 'FCFS':
            result = FCFS.FCFS(self.process_data)
        elif algorithm == 'MLFQ':
            quantum = self.get_quantum()
            if quantum is None:
                return
            result = MLFQ.multilevel_feedback(self.process_data, quantum)
        elif algorithm == 'RR':
            quantum = self.get_quantum()
            if quantum is None:
                return
            result = RR.RR(self.process_data, quantum)                     
        else:
            messagebox.showerror("Error", f"Algorithm {algorithm} is not implemented.")
            return

        # Display the results in text
        self.result_text.insert(tk.END, "Execution Order:\n")
        for step in result['execution_order']:
            self.result_text.insert(tk.END, f"Time: {step['time']}, Process ID: {step['proc_id']}\n")

        self.result_text.insert(tk.END, f"\nAverage Waiting Time: {result['average_waiting_time']:.2f}\n")
        self.result_text.insert(tk.END, f"Average Turnaround Time: {result['average_turnaround_time']:.2f}\n")
        self.result_text.insert(tk.END, f"Total Execution Time: {result['total_execution_time']}\n")

        # Draw Gantt chart
        self.draw_gantt_chart(result['execution_order'], result['total_execution_time'])

    def draw_gantt_chart(self, execution_order, total_execution_time):
        """Draw a Gantt chart based on the execution order."""
        if hasattr(self, 'chart_canvas'):
            self.chart_canvas.get_tk_widget().pack_forget()

        fig, ax = plt.subplots(figsize=(10, 5))

        # To track the total time
        current_time = 0
        execution_segments = []

        for index, entry in enumerate(execution_order):
            proc_id = entry['proc_id']
            
            # Calculate execution time for the current process
            if proc_id is not None:
                # If not the last entry, take the time of the next entry to calculate duration
                if index < len(execution_order) - 1:
                    next_time = execution_order[index + 1]['time']
                    execution_time = next_time - current_time
                else:
                    # For the last entry, assume it runs till the end (or set a default)
                    execution_time = total_execution_time-current_time

                execution_segments.append((current_time, execution_time, proc_id))
            
            # Update current time
            current_time += execution_time

        # Plot each process' segments
        for start_time, exec_time, proc_id in execution_segments:
            ax.broken_barh([(start_time, exec_time)], (proc_id * 10, 9), facecolors='blue')

        # Configure the Gantt chart
        ax.set_xlabel('Time')
        ax.set_ylabel('Process ID')
        ax.set_yticks([i * 10 + 5 for i in range(len(self.process_data))])
        ax.set_yticklabels([f"Process {i}" for i in range(len(self.process_data))])
        ax.grid(True)

        # Embedding the plot into Tkinter canvas
        self.chart_canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        self.chart_canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()