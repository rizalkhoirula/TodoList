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

    def add_task(self, title, user_id, due_date=None, priority='Medium', category_id=None, parent_task_id=None, recurring_type=None, recurring_end_date=None):
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")

        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Due date must be in YYYY-MM-DD format.")

        if recurring_end_date:
            try:
                datetime.strptime(recurring_end_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Recurring end date must be in YYYY-MM-DD format.")

        query = """
            INSERT INTO tasks
            (title, user_id, due_date, priority, category_id, parent_task_id, recurring_type, recurring_end_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (title, user_id, due_date, priority, category_id, parent_task_id, recurring_type, recurring_end_date))
        self.conn.commit()

    def fetch_tasks(self, user_id, order_by=None, filter_criteria=None, search_term=None):
        params = [user_id]
        base_query = "SELECT id, title, completed, due_date, priority, category_id, parent_task_id, recurring_type, recurring_end_date FROM tasks WHERE user_id = %s"

        where_clauses = []
        if filter_criteria:
            for key, value in filter_criteria.items():
                if value is None or (isinstance(value, str) and str(value).lower() == 'all'): # Skip 'all' or None filters
                    continue
                # Ensure key is a valid column name
                if key == "completed":
                    where_clauses.append(f"{key} = %s")
                    params.append(bool(value))
                elif key == "priority":
                    where_clauses.append(f"{key} = %s")
                    params.append(value)
                elif key == "category_id":
                    if value == "" or value is None : continue # Skip if empty string or None from combobox
                    where_clauses.append(f"{key} = %s")
                    params.append(int(value))

        if search_term and search_term.strip():
            # Add search term to where clauses, searching in title
            # Potentially add more fields to search in, e.g., description if it existed
            where_clauses.append("title LIKE %s")
            params.append(f"%{search_term.strip()}%")


        if where_clauses:
            base_query += " AND " + " AND ".join(where_clauses)

        if order_by:
            # Validate order_by to prevent SQL injection. It should be a column name and optional ASC/DESC.
            # Example: "due_date ASC", "priority DESC"
            # Simple validation: check if column part is in a list of allowed columns.
            allowed_sort_cols = ["id", "title", "due_date", "priority", "completed"]
            col_name = order_by.split()[0].lower()
            if col_name in allowed_sort_cols:
                # Further ensure direction is ASC or DESC if present
                if len(order_by.split()) > 1 and order_by.split()[1].upper() not in ["ASC", "DESC"]:
                     # default or raise error if direction is invalid
                     base_query += f" ORDER BY {col_name} ASC" # Default to ASC
                else:
                    base_query += f" ORDER BY {order_by}"
            else: # Default sort if order_by is not valid/safe
                base_query += " ORDER BY id DESC" # Ensure default sort is applied if order_by is invalid
        else:
            base_query += " ORDER BY id DESC" # Default sort if no order_by is provided

        self.cursor.execute(base_query, tuple(params))
        return self.cursor.fetchall()

    def update_task(self, task_id, new_title=None, new_due_date=None, new_priority=None, new_category_id=None, new_parent_task_id=None, new_recurring_type=None, new_recurring_end_date=None, new_completed_status: bool = None):
        # This version allows updating specific fields by only including them if they are not None
        # However, for nullable fields in DB, client needs to pass explicit None to set them to NULL vs. not changing them.
        # For this subtask, we'll assume any parameter passed (even if None) is intended for update.
        # A more robust way would be to pass a dict of fields_to_update.

        update_fields = {}
        if new_title is not None: # Title usually shouldn't be set to empty, but None might mean "don't change"
            update_fields["title"] = new_title
        if new_due_date is not None: # Allow explicit NULL
             if isinstance(new_due_date, str): # Validate if string
                try:
                    datetime.strptime(new_due_date, "%Y-%m-%d")
                except ValueError:
                    raise ValueError("New due date must be in YYYY-MM-DD format.")
             update_fields["due_date"] = new_due_date
        elif 'new_due_date' in locals() and new_due_date is None: # Explicitly passed as None
            update_fields["due_date"] = None

        if new_priority is not None:
            update_fields["priority"] = new_priority

        # For nullable foreign keys and other fields, explicit None means set to NULL
        if 'new_category_id' in locals(): # Check if arg was passed
            update_fields["category_id"] = new_category_id
        if 'new_parent_task_id' in locals():
            update_fields["parent_task_id"] = new_parent_task_id
        if 'new_recurring_type' in locals():
             update_fields["recurring_type"] = new_recurring_type if new_recurring_type != 'None' else None # Handle 'None' string from combobox
        if 'new_recurring_end_date' in locals():
            if new_recurring_end_date:
                if isinstance(new_recurring_end_date, str):
                    try:
                        datetime.strptime(new_recurring_end_date, "%Y-%m-%d")
                    except ValueError:
                        raise ValueError("New recurring end date must be in YYYY-MM-DD format.")
                update_fields["recurring_end_date"] = new_recurring_end_date
            else: # Explicit None or empty string
                 update_fields["recurring_end_date"] = None


        if new_completed_status is not None:
            update_fields["completed"] = bool(new_completed_status)

        if not update_fields:
            # Or raise ValueError("No fields to update")
            return 0 # No update performed

        set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
        params = list(update_fields.values())
        params.append(task_id)

        query = f"UPDATE tasks SET {set_clause} WHERE id = %s"

        self.cursor.execute(query, tuple(params))
        self.conn.commit()
        return self.cursor.rowcount # Return number of rows affected

    def get_task_by_id(self, task_id, user_id):
        query = "SELECT * FROM tasks WHERE id = %s AND user_id = %s"
        self.cursor.execute(query, (task_id, user_id))
        return self.cursor.fetchone()

    def delete_task(self, task_id): # Assuming task_id is globally unique or further checks are in controller
        query = "DELETE FROM tasks WHERE id = %s"
        self.cursor.execute(query, (task_id,))
        self.conn.commit()

    # Modified to set completed status to True or False
    def mark_task_status(self, task_id, completed_status: bool):
        query = "UPDATE tasks SET completed = %s WHERE id = %s"
        self.cursor.execute(query, (completed_status, task_id))
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

    # Category CRUD methods
    def add_category(self, name, user_id):
        name = name.strip()
        if not name:
            raise ValueError("Category name cannot be empty.")
        try:
            query = "INSERT INTO categories (name, user_id) VALUES (%s, %s)"
            self.cursor.execute(query, (name, user_id))
            self.conn.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            # Assuming IntegrityError for duplicate name (unique constraint)
            # You might need to check err.errno for specific MySQL error codes
            if "Duplicate entry" in str(err) or (hasattr(err, 'errno') and err.errno == 1062):
                 raise ValueError(f"A category with the name '{name}' already exists.")
            raise # Re-raise other errors

    def fetch_categories(self, user_id):
        query = "SELECT id, name FROM categories WHERE user_id = %s ORDER BY name ASC"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def get_category_by_id(self, category_id, user_id):
        query = "SELECT id, name FROM categories WHERE id = %s AND user_id = %s"
        self.cursor.execute(query, (category_id, user_id))
        return self.cursor.fetchone()

    def fetch_task_list_for_selection(self, user_id, exclude_task_id=None):
        """
        Fetches tasks (id, title) for a user, optionally excluding a specific task ID.
        Used to populate 'Parent Task' selection dropdowns.
        """
        params = [user_id]
        query = "SELECT id, title FROM tasks WHERE user_id = %s"
        if exclude_task_id is not None:
            query += " AND id != %s"
            params.append(exclude_task_id)
        query += " ORDER BY title ASC" # Or by creation date, etc.

        self.cursor.execute(query, tuple(params))
        return self.cursor.fetchall()

    def update_category(self, category_id, user_id, new_name):
        new_name = new_name.strip()
        if not new_name:
            raise ValueError("New category name cannot be empty.")
        try:
            query = "UPDATE categories SET name = %s WHERE id = %s AND user_id = %s"
            self.cursor.execute(query, (new_name, category_id, user_id))
            self.conn.commit()
            return self.cursor.rowcount > 0 # Returns True if update happened
        except mysql.connector.Error as err:
            if "Duplicate entry" in str(err) or (hasattr(err, 'errno') and err.errno == 1062):
                raise ValueError(f"Another category with the name '{new_name}' already exists.")
            raise

    def delete_category(self, category_id, user_id):
        # Consider impact on tasks: either set task.category_id to NULL (if allowed)
        # or prevent deletion if category is in use, or delete/unassign tasks.
        # For now, direct delete. Schema should define ON DELETE SET NULL or ON DELETE RESTRICT for tasks.category_id.
        # Assuming tasks.category_id can be NULL or is handled by ON DELETE SET NULL in DB schema.
        query = "DELETE FROM categories WHERE id = %s AND user_id = %s"
        self.cursor.execute(query, (category_id, user_id))
        self.conn.commit()
        return self.cursor.rowcount > 0 # Returns True if delete happened

    def close(self):
        self.cursor.close()
        self.conn.close()
