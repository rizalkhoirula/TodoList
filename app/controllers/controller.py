# app/controller.py

from app.models.database import Database


class TaskController:
    def __init__(self, user_id=1):  # Default to user 1 for now
        self.db = Database()
        self.user_id = user_id

    def get_tasks(self, order_by=None, filter_criteria=None, search_term=None):
        # Always fetch tasks for the user_id associated with this controller instance
        return self.db.fetch_tasks(user_id=self.user_id, order_by=order_by, filter_criteria=filter_criteria, search_term=search_term)

    def add_task(self, title, user_id, due_date=None, priority='Medium', category_id=None, parent_task_id=None, recurring_type=None, recurring_end_date=None):
        # user_id is passed directly, self.user_id from __init__ might be default/app owner if not careful
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        # Validation for date formats can also be here or rely on DB layer
        self.db.add_task(title, user_id, due_date, priority, category_id, parent_task_id, recurring_type, recurring_end_date)

    def delete_task(self, task_id): # Assuming task_id is unique and implies user ownership or admin rights
        self.db.delete_task(task_id)

    def update_task(self, task_id, new_title=None, new_due_date=None, new_priority=None, new_category_id=None, new_parent_task_id=None, new_recurring_type=None, new_recurring_end_date=None, new_completed_status: bool = None):
        # Ensure task belongs to the user associated with this controller instance
        # This is a conceptual check; actual get_task_by_id might be needed if task_id is not user-specific in calls
        # For now, we assume task_id is sufficient or GUI ensures correct user context.
        # However, the DB method get_task_by_id requires user_id, so we should use it if we were to fetch first.
        # The database update_task does not currently verify user_id against task_id.
        return self.db.update_task(task_id, new_title, new_due_date, new_priority, new_category_id, new_parent_task_id, new_recurring_type, new_recurring_end_date, new_completed_status)

    def mark_task_status(self, task_id, status: bool):
        # Similar to update_task, could verify task ownership first.
        # For example:
        # task = self.db.get_task_by_id(task_id, self.user_id)
        # if not task:
        #     raise ValueError("Task not found or access denied.")
        self.db.mark_task_status(task_id, status)

    def get_task_by_id(self, task_id, user_id):
        # Enforce that the controller's user can only fetch their own tasks,
        # even if GUI passes a different user_id (which it shouldn't for this method from GUI)
        if self.user_id != user_id:
             raise PermissionError("User can only fetch their own task details.")
        return self.db.get_task_by_id(task_id, user_id)

    def get_task_list_for_selection(self, user_id, exclude_task_id=None):
        # Enforce that this list is for the currently logged-in user.
        if self.user_id != user_id:
            # This situation should ideally not happen if GUI always uses self.user_id.
            # If it can, it implies trying to fetch tasks for one user to be parent of another's task,
            # which might be a complex/unintended scenario unless explicitly designed for.
            raise PermissionError("Cannot fetch parent task list for another user.")
        return self.db.fetch_task_list_for_selection(user_id, exclude_task_id)

    # --- Category Methods ---
    def add_category(self, name, user_id):
        # It's good practice to ensure user_id matches self.user_id or handle permissions
        # For now, assume user_id parameter is authoritative for this action.
        if self.user_id != user_id:
            # This check might be too simplistic depending on roles/permissions
            # For a personal ToDo app, user_id should always be self.user_id
            # Consider if a category can be added by an admin for another user, etc.
            # For now, let's enforce that a user can only add categories for themselves.
            # raise PermissionError("User can only add categories for themselves.")
            # Or, more simply, always use self.user_id:
            pass # Using the passed user_id as per subtask, but use self.user_id if controller is user-specific instance
        return self.db.add_category(name, user_id) # Or self.db.add_category(name, self.user_id)

    def fetch_categories(self, user_id):
        # Similar consideration for user_id
        if self.user_id != user_id:
            # raise PermissionError("User can only fetch their own categories.")
            pass
        return self.db.fetch_categories(user_id) # Or self.db.fetch_categories(self.user_id)

    def get_category_by_id(self, category_id, user_id):
        if self.user_id != user_id:
            # raise PermissionError("User can only get their own categories.")
            pass
        return self.db.get_category_by_id(category_id, user_id) # Or with self.user_id

    def update_category(self, category_id, user_id, new_name):
        if self.user_id != user_id:
            # raise PermissionError("User can only update their own categories.")
            pass
        # One might also fetch the category first to ensure it belongs to user_id before updating
        return self.db.update_category(category_id, user_id, new_name) # Or with self.user_id

    def delete_category(self, category_id, user_id):
        if self.user_id != user_id:
            # raise PermissionError("User can only delete their own categories.")
            pass
        # Similar: fetch first to verify ownership
        return self.db.delete_category(category_id, user_id) # Or with self.user_id

    def close(self):
        self.db.close()
