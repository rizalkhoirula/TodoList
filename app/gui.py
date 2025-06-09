# app/gui.py

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from app.controller import TaskController
from tkcalendar import DateEntry


class ToDoApp:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("To-Do App")
        self.controller = TaskController(user_id=user_id)
        self.tasks = []

        self._build_ui()
        self._load_tasks()

    def _build_ui(self):
        # Entry frame
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(pady=10)

        # Task title input
        self.task_entry = tk.Entry(entry_frame, width=30)
        self.task_entry.pack(side=tk.LEFT, padx=(0, 10))

        # Due date checkbox + calendar
        self.no_due_date_var = tk.BooleanVar(value=False)
        self.no_due_date_cb = tk.Checkbutton(entry_frame, text="No Due Date", variable=self.no_due_date_var,
                                             command=self._toggle_due_date)
        self.no_due_date_cb.pack(side=tk.LEFT, padx=(0, 5))

        self.due_date_entry = DateEntry(entry_frame, width=12, background='darkblue',
                                        foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.due_date_entry.pack(side=tk.LEFT, padx=(0, 10))

        # Priority dropdown
        self.priority_var = tk.StringVar(value='Medium')
        priority_options = ['Low', 'Medium', 'High']
        self.priority_menu = ttk.Combobox(entry_frame, textvariable=self.priority_var, values=priority_options, width=10)
        self.priority_menu.pack(side=tk.LEFT, padx=(0, 10))

        # Add Task button
        add_btn = tk.Button(entry_frame, text="Add Task", command=self.add_task)
        add_btn.pack(side=tk.LEFT)

        # Listbox with scrollbar
        list_frame = tk.Frame(self.root)
        list_frame.pack(padx=10, pady=10)

        self.task_listbox = tk.Listbox(list_frame, width=70, height=15)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        # Button frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        delete_btn = tk.Button(btn_frame, text="Delete Task", command=self.delete_task)
        delete_btn.pack(side=tk.LEFT, padx=5)

        done_btn = tk.Button(btn_frame, text="Mark Done", command=self.mark_done)
        done_btn.pack(side=tk.LEFT, padx=5)

        edit_btn = tk.Button(btn_frame, text="Edit Task", command=self.edit_task)
        edit_btn.pack(side=tk.LEFT, padx=5)

    def _toggle_due_date(self):
        if self.no_due_date_var.get():
            self.due_date_entry.config(state='disabled')
        else:
            self.due_date_entry.config(state='normal')

    def _parse_due_date(self, raw_due_date):
        if raw_due_date is None:
            return datetime.max.date()
        if isinstance(raw_due_date, datetime):
            return raw_due_date.date()
        if isinstance(raw_due_date, str):
            try:
                return datetime.strptime(raw_due_date, "%Y-%m-%d").date()
            except ValueError:
                try:
                    return datetime.fromisoformat(raw_due_date).date()
                except ValueError:
                    pass
        return datetime.max.date()

    def _load_tasks(self):
        self.tasks = self.controller.get_all_tasks()
        self.task_listbox.delete(0, tk.END)

        today = datetime.today().date()

        self.tasks.sort(key=lambda task: (
            self._parse_due_date(task["due_date"]),
            task["completed"]
        ))

        for task in self.tasks:
            title = task["title"]
            completed = task["completed"]
            due_date = task["due_date"]
            priority = task.get("priority", "Medium")

            status = "✓ " if completed else "[ ] "

            if due_date:
                try:
                    due_dt = datetime.strptime(str(due_date), "%Y-%m-%d").date()
                    due_str = due_dt.strftime("%Y-%m-%d")
                except Exception:
                    due_dt = None
                    due_str = str(due_date).split()[0]
            else:
                due_dt = None
                due_str = "No due date"

            display_text = f"{status}{title} (Due: {due_str}, Priority: {priority})"
            self.task_listbox.insert(tk.END, display_text)

            if not completed and due_dt:
                if due_dt < today:
                    self.task_listbox.itemconfig(tk.END, {'fg': 'red'})
                elif due_dt == today:
                    self.task_listbox.itemconfig(tk.END, {'fg': 'orange'})

    def add_task(self):
        title = self.task_entry.get().strip()
        priority = self.priority_var.get()

        if self.no_due_date_var.get():
            due_date = None
        else:
            due_date = self.due_date_entry.get().strip()
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Input Error", "Due date must be in YYYY-MM-DD format.")
                return

        if not title:
            messagebox.showwarning("Input Error", "Task title cannot be empty.")
            return

        try:
            self.controller.add_task(title, due_date, priority)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.task_entry.delete(0, tk.END)
        self.no_due_date_var.set(False)
        self._toggle_due_date()
        self.priority_var.set("Medium")
        self._load_tasks()

    def delete_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected task?")
        if not confirm:
            return

        task = self.tasks[selection[0]]
        task_id = task["id"]

        try:
            self.controller.delete_task(task_id)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete task: {e}")
            return

        self._load_tasks()

    def edit_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a task to edit.")
            return

        task = self.tasks[selection[0]]
        task_id = task["id"]
        current_title = task["title"]
        current_due = task["due_date"]
        current_priority = task.get("priority", "Medium")

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")

        tk.Label(edit_window, text="Title:").pack(pady=(10, 0))
        title_entry = tk.Entry(edit_window, width=40)
        title_entry.insert(0, current_title)
        title_entry.pack(pady=(0, 10))

        tk.Label(edit_window, text="Due Date (YYYY-MM-DD or leave blank):").pack()
        due_entry = DateEntry(edit_window, width=12, background='darkblue',
                              foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        if current_due:
            try:
                due_entry.set_date(current_due)
            except:
                pass
        due_entry.pack(pady=(0, 10))

        tk.Label(edit_window, text="Priority:").pack()
        priority_var = tk.StringVar(edit_window)
        priority_options = ['Low', 'Medium', 'High']
        priority_dropdown = ttk.Combobox(edit_window, textvariable=priority_var, values=priority_options, width=15)
        priority_dropdown.pack(pady=(0, 10))
        priority_var.set(current_priority)

        def save_changes():
            new_title = title_entry.get().strip()
            new_due = due_entry.get().strip()
            new_priority = priority_var.get()

            if new_due == "":
                new_due = None
            else:
                try:
                    datetime.strptime(new_due, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Invalid Date", "Please use YYYY-MM-DD format.")
                    return

            if not new_title:
                messagebox.showerror("Invalid Title", "Task title cannot be empty.")
                return

            try:
                self.controller.update_task(task_id, new_title, new_due, new_priority)
                self._load_tasks()
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Update Failed", str(e))

        save_btn = tk.Button(edit_window, text="Save", command=save_changes)
        save_btn.pack(pady=10)

    def mark_done(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a task to mark as done.")
            return

        task = self.tasks[selection[0]]
        task_id = task["id"]

        try:
            self.controller.mark_task_done(task_id)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to mark task as done: {e}")
            return

        self._load_tasks()


def launch_gui(user_id):
    root = tk.Tk()
    app = ToDoApp(root, user_id)
    root.mainloop()
