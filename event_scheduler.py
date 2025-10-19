import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# Parse time (HH:MM)
def parse_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M")
    except ValueError:
        return None

# Detect conflicts
def check_conflicts(events):
    conflicts = []
    for i in range(len(events)):
        for j in range(i + 1, len(events)):
            e1, e2 = events[i], events[j]
            if e1['start'] < e2['end'] and e2['start'] < e1['end']:
                conflicts.append((e1['name'], e2['name']))
    return conflicts

# Add event function
def add_event():
    name = event_name.get().strip()
    start = start_time.get().strip()
    end = end_time.get().strip()

    if not name or not start or not end:
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return

    s_time = parse_time(start)
    e_time = parse_time(end)

    if not s_time or not e_time:
        messagebox.showerror("Time Format Error", "Use HH:MM format for time.")
        return

    if s_time >= e_time:
        messagebox.showerror("Invalid Time", "End time must be after start time.")
        return

    events.append({'name': name, 'start': s_time, 'end': e_time})
    events.sort(key=lambda x: x['start'])

    update_table()
    event_name.delete(0, tk.END)
    start_time.delete(0, tk.END)
    end_time.delete(0, tk.END)

# Show conflicts and free slots
def analyze_schedule():
    if not events:
        messagebox.showinfo("Info", "No events added yet!")
        return

    conflicts = check_conflicts(events)
    if conflicts:
        result = "⚠️ Conflicting Events:\n\n"
        for c in conflicts:
            result += f"- {c[0]} and {c[1]}\n"
    else:
        result = "✅ No conflicts detected!\n"

    # Free slots
    result += "\n--- Free Time Slots ---\n"
    for i in range(len(events) - 1):
        end_current = events[i]['end']
        start_next = events[i + 1]['start']
        if end_current < start_next:
            result += f"{end_current.strftime('%H:%M')} - {start_next.strftime('%H:%M')}\n"

    messagebox.showinfo("Schedule Analysis", result)

# Update table view
def update_table():
    for row in tree.get_children():
        tree.delete(row)
    for e in events:
        tree.insert("", "end", values=(e['name'], e['start'].strftime("%H:%M"), e['end'].strftime("%H:%M")))

# Clear all events
def clear_all():
    events.clear()
    update_table()
    messagebox.showinfo("Cleared", "All events have been cleared.")

# Main GUI window
root = tk.Tk()
root.title("Event Scheduler and Conflict Detector")
root.geometry("600x500")
root.config(bg="#f2f2f2")

events = []

# Heading
tk.Label(root, text="Event Scheduler and Conflict Detector", font=("Helvetica", 16, "bold"), bg="#f2f2f2", fg="#333").pack(pady=10)

# Input Frame
frame = tk.Frame(root, bg="#f2f2f2")
frame.pack(pady=10)

tk.Label(frame, text="Event Name:", bg="#f2f2f2").grid(row=0, column=0, padx=5, pady=5)
event_name = tk.Entry(frame, width=25)
event_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Start Time (HH:MM):", bg="#f2f2f2").grid(row=1, column=0, padx=5, pady=5)
start_time = tk.Entry(frame, width=25)
start_time.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="End Time (HH:MM):", bg="#f2f2f2").grid(row=2, column=0, padx=5, pady=5)
end_time = tk.Entry(frame, width=25)
end_time.grid(row=2, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text="Add Event", command=add_event, bg="#4CAF50", fg="white", width=15).pack(pady=5)
tk.Button(root, text="Analyze Schedule", command=analyze_schedule, bg="#2196F3", fg="white", width=15).pack(pady=5)
tk.Button(root, text="Clear All", command=clear_all, bg="#f44336", fg="white", width=15).pack(pady=5)

# Table for events
columns = ("Event Name", "Start Time", "End Time")
tree = ttk.Treeview(root, columns=columns, show="headings", height=8)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)
tree.pack(pady=10)

root.mainloop()
