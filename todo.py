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
                # Add default priority to older tasks
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

# -------- Menu Functions --------


def show_menu():
    print("\n==== TO-DO LIST ====")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Pending Tasks")
    print("4. View Completed Tasks")
    print("5. Mark Task as Done")
    print("6. Delete Task")
    print("7. Exit")


def add_task():
    task = input("Enter task: ")
    priority = input("Enter priority (High/Medium/Low): ").capitalize()
    if priority not in ["High", "Medium", "Low"]:
        print("Invalid priority. Defaulting to Medium.")
        priority = "Medium"
    tasks.append({"task": task, "done": False, "priority": priority})
    save_tasks()
    print("Task added!")


def view_tasks(filter_status=None):
    filtered = tasks
    if filter_status == "pending":
        filtered = [t for t in tasks if not t["done"]]
    elif filter_status == "done":
        filtered = [t for t in tasks if t["done"]]

    if not filtered:
        print("No tasks to show.")
        return

    # Sort by priority: High > Medium > Low
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    filtered.sort(key=lambda x: priority_order.get(x["priority"], 4))

    for idx, task in enumerate(filtered, start=1):
        status = "✓" if task["done"] else "✗"
        print(f"{idx}. [{status}] ({task['priority']}) {task['task']}")


def mark_done():
    view_tasks("pending")
    try:
        index = int(input("Enter task number to mark as done: ")) - 1
        pending = [t for t in tasks if not t["done"]]
        if 0 <= index < len(pending):
            task_to_mark = pending[index]
            for t in tasks:
                if t == task_to_mark:
                    t["done"] = True
                    break
            save_tasks()
            print("Task marked as done!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


def delete_task():
    view_tasks()
    try:
        index = int(input("Enter task number to delete: ")) - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            save_tasks()
            print(f"Deleted: {removed['task']}")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


# -------- Main Program --------
load_tasks()

while True:
    show_menu()
    choice = input("Enter choice (1-7): ")

    if choice == '1':
        add_task()
    elif choice == '2':
        view_tasks()
    elif choice == '3':
        view_tasks("pending")
    elif choice == '4':
        view_tasks("done")
    elif choice == '5':
        mark_done()
    elif choice == '6':
        delete_task()
    elif choice == '7':
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Try again.")
