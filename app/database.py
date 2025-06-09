# app/database.py

import mysql.connector
import bcrypt
from datetime import datetime


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='todo_db'
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def add_task(self, title, due_date=None, user_id=1, priority='Medium'):
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")

        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Due date must be in YYYY-MM-DD format.")

        query = "INSERT INTO tasks (title, due_date, user_id, priority) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (title, due_date, user_id, priority))
        self.conn.commit()

    def fetch_tasks(self, user_id=1):
        query = "SELECT id, title, completed, due_date, priority FROM tasks WHERE user_id = %s ORDER BY id DESC"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def update_task(self, task_id, new_title, new_due_date, new_priority='Medium'):
        if new_due_date:
            try:
                datetime.strptime(new_due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Due date must be in YYYY-MM-DD format.")
        else:
            new_due_date = None

        query = "UPDATE tasks SET title = %s, due_date = %s, priority = %s WHERE id = %s"
        self.cursor.execute(query, (new_title, new_due_date, new_priority, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = %s"
        self.cursor.execute(query, (task_id,))
        self.conn.commit()

    def mark_task_done(self, task_id):
        query = "UPDATE tasks SET completed = TRUE WHERE id = %s"
        self.cursor.execute(query, (task_id,))
        self.conn.commit()

    def check_user_credentials(self, username, password):
        query = "SELECT id, password_hash FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()

        if result and bcrypt.checkpw(password.encode('utf-8'), result['password_hash'].encode('utf-8')):
            return result['id']
        return None

    def register_user(self, username, email, password):
        self.cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
        if self.cursor.fetchone():
            raise ValueError("Username or email already exists.")

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (username, email, hashed))
        self.conn.commit()

    def get_user_by_username(self, username):
        query = "SELECT id, username, password_hash FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()

    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE email = %s"
        self.cursor.execute(query, (email,))
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()
