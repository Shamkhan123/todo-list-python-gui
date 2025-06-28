from functools import partial
import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "tasks.json"
tasks = []

# -------- File Handling --------


def load_tasks():
    global tasks
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            try:
                tasks = json.load(file)
                for task in tasks:
                    if "priority" not in task:
                        task["priority"] = "Medium"
            except json.JSONDecodeError:
                tasks = []
    else:
        tasks = []


def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

# -------- Task Functions --------


def add_task():
    task_text = task_entry.get().strip()
    if not task_text:
        messagebox.showwarning("Empty Task", "Please enter a task.")
        return

    priority = priority_var.get()
    tasks.append({"task": task_text, "done": False, "priority": priority})
    save_tasks()
    task_entry.delete(0, tk.END)
    refresh_list()


def mark_done(index):
    tasks[index]["done"] = not tasks[index]["done"]
    save_tasks()
    refresh_list()


def delete_task(index):
    del tasks[index]
    save_tasks()
    refresh_list()

# -------- GUI Update --------


def refresh_list():
    for widget in task_frame.winfo_children():
        widget.destroy()

    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    sorted_tasks = sorted(tasks, key=lambda x: (
        x["done"], priority_order.get(x["priority"], 4)))

    for task in sorted_tasks:
        row = tk.Frame(task_frame)
        row.pack(fill="x", padx=5, pady=2)

        # Bind BooleanVar to the actual task's done value
        status_var = tk.BooleanVar(value=task["done"])

        # When the var changes, this callback is triggered
        def on_check(var=status_var, task_ref=task):
            task_ref["done"] = var.get()
            save_tasks()

        # Attach trace listener to the BooleanVar
        status_var.trace_add("write", lambda *_: on_check())

        chk = tk.Checkbutton(
            row,
            variable=status_var
        )
        chk.pack(side="left")

        lbl = tk.Label(
            row, text=f"[{task['priority']}] {task['task']}", anchor="w", width=40)
        lbl.pack(side="left")

        del_btn = tk.Button(row, text="Delete",
                            command=partial(delete_task_direct, task))
        del_btn.pack(side="right")


def toggle_task(task):
    task["done"] = not task["done"]
    save_tasks()
    refresh_list()


def delete_task_direct(task):
    tasks.remove(task)
    save_tasks()
    refresh_list()


# -------- GUI Setup --------
load_tasks()
root = tk.Tk()
root.title("To-Do List")

# Input row
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

task_entry = tk.Entry(input_frame, width=30)
task_entry.pack(side="left", padx=(0, 5))

priority_var = tk.StringVar(value="Medium")
priority_menu = tk.OptionMenu(
    input_frame, priority_var, "High", "Medium", "Low")
priority_menu.pack(side="left", padx=(0, 5))

add_btn = tk.Button(input_frame, text="Add Task", command=add_task)
add_btn.pack(side="left")

# Task list
task_frame = tk.Frame(root)
task_frame.pack(fill="both", expand=True, padx=10, pady=10)

refresh_list()
root.mainloop()
