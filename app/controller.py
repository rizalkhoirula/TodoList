# app/controller.py

from app.database import Database


class TaskController:
    def __init__(self, user_id=1):  # Default to user 1 for now
        self.db = Database()
        self.user_id = user_id

    def get_all_tasks(self):
        return self.db.fetch_tasks(user_id=self.user_id)

    def add_task(self, title, due_date=None, priority='Medium'):
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        self.db.add_task(title, due_date, user_id=self.user_id, priority=priority)

    def delete_task(self, task_id):
        self.db.delete_task(task_id)

    def update_task(self, task_id, new_title, new_due_date, new_priority='Medium'):
        self.db.update_task(task_id, new_title, new_due_date, new_priority)

    def mark_task_done(self, task_id):
        self.db.mark_task_done(task_id)

    def close(self):
        self.db.close()
