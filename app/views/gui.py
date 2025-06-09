# app/gui.py

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from app.controllers.controller import TaskController
from tkcalendar import DateEntry


class ToDoApp:
    def __init__(self, root, user_id, on_logout_callback=None):
        self.root = root
        self.user_id = user_id
        self.on_logout_callback = on_logout_callback
        self.root.title("Modern To-Do App")
        self.root.geometry("1200x700")
        self.controller = TaskController(user_id=self.user_id)

        self.current_theme = 'light' # Default theme
        self.current_search_term = "" # Initialize search term
        self._define_themes()

        self._configure_styles() # Apply initial theme
        self._build_ui()
        self._show_view_tasks()

    def _define_themes(self):
        self.themes = {
            'light': {
                "sidebar_bg": "#34495e",
                "sidebar_fg": "white", # Button text on sidebar
                "sidebar_button_active_bg": "#4a6fa5",
                "content_bg": "#f4f6f7",
                "content_fg": "black", # General text in content area
                "button_bg": "#5dade2", # General ttk buttons
                "button_fg": "white",
                "entry_bg": "white",
                "entry_fg": "black",
                "entry_insert": "black", # Cursor color
                "tree_bg": "white",
                "tree_fg": "black", # Treeview item text
                "tree_heading_bg": "#5dade2",
                "tree_heading_fg": "white",
                "tree_selected_bg": "#a9d0f5", # When a treeview row is selected
                "text_color": "black",
                "disabled_fg": "grey",
                "dialog_bg": "#e0e0e0", # Dialog background
                "label_fg": "black" # General label text color
            },
            'dark': {
                "sidebar_bg": "#2c3e50",
                "sidebar_fg": "#ecf0f1",
                "sidebar_button_active_bg": "#34495e",
                "content_bg": "#34495e", # Darker content area
                "content_fg": "#ecf0f1",
                "button_bg": "#528b8b", # Tealish buttons
                "button_fg": "#ecf0f1",
                "entry_bg": "#2c3e50",
                "entry_fg": "#ecf0f1",
                "entry_insert": "white",
                "tree_bg": "#2c3e50",
                "tree_fg": "#ecf0f1",
                "tree_heading_bg": "#528b8b",
                "tree_heading_fg": "#ecf0f1",
                "tree_selected_bg": "#4a6fa5",
                "text_color": "#ecf0f1",
                "disabled_fg": "grey",
                "dialog_bg": "#2c3e50",
                "label_fg": "#ecf0f1"
            }
        }
        # Store initial colors for non-ttk widgets that might be referenced directly
        self.colors = self.themes[self.current_theme]


    def _configure_styles(self, theme_name=None):
        if theme_name is None:
            theme_name = self.current_theme

        active_theme = self.themes[theme_name]
        self.colors = active_theme # Update self.colors to current theme for direct use

        self.style = ttk.Style()
        self.style.theme_use('clam')

        # General TButton style
        self.style.configure("TButton",
                             padding=6, relief="flat",
                             font=('Helvetica', 10),
                             background=active_theme["button_bg"],
                             foreground=active_theme["button_fg"])
        self.style.map("TButton",
                       background=[('active', active_theme["sidebar_button_active_bg"])])


        # Sidebar Button style
        self.style.configure("Sidebar.TButton",
                             background=active_theme["sidebar_bg"],
                             foreground=active_theme["sidebar_fg"],
                             width=20,
                             font=('Helvetica', 11, 'bold'),
                             padding=(10,10),
                             relief="flat")
        self.style.map("Sidebar.TButton",
                       background=[('active', active_theme["sidebar_button_active_bg"])])

        # Treeview style
        self.style.configure("Treeview.Heading",
                             background=active_theme["tree_heading_bg"],
                             foreground=active_theme["tree_heading_fg"],
                             font=('Helvetica', 10, 'bold'),
                             relief="flat")
        self.style.configure("Treeview",
                             background=active_theme["tree_bg"],
                             foreground=active_theme["tree_fg"],
                             fieldbackground=active_theme["tree_bg"], # Background of the data area
                             rowheight=25,
                             font=('Helvetica', 9))
        self.style.map("Treeview",
                       background=[('selected', active_theme["tree_selected_bg"])],
                       foreground=[('selected', active_theme["tree_fg"])]) # Ensure text on selected is readable
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) # Remove border

        # Combobox style
        self.style.configure("TCombobox",
                             fieldbackground=active_theme["entry_bg"],
                             background=active_theme["entry_bg"], # button color
                             foreground=active_theme["entry_fg"],
                             arrowcolor=active_theme["text_color"],
                             insertcolor=active_theme["entry_insert"],
                             selectbackground=active_theme["tree_selected_bg"], # dropdown selection bg
                             selectforeground=active_theme["entry_fg"])

        # Entry style
        self.style.configure("TEntry",
                             fieldbackground=active_theme["entry_bg"],
                             foreground=active_theme["entry_fg"],
                             insertcolor=active_theme["entry_insert"])

        # Frame style for content area sections (if needed for consistent bg)
        self.style.configure("Content.TFrame", background=active_theme["content_bg"])


    def _build_ui(self):
        # Apply theme to root window
        self.root.config(bg=self.colors["content_bg"])

        # Sidebar Frame
        self.sidebar_frame = tk.Frame(self.root, width=200, bg=self.colors["sidebar_bg"])
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)

        # Content Frame
        self.content_frame = tk.Frame(self.root, bg=self.colors["content_bg"])
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Sidebar Buttons ---
        # Menu Label (tk.Label, so needs manual config)
        self.menu_label = tk.Label(self.sidebar_frame, text="Menu", font=('Helvetica', 16, 'bold'),
                                   bg=self.colors["sidebar_bg"], fg=self.colors["sidebar_fg"])
        self.menu_label.pack(pady=20)

        tasks_button = ttk.Button(self.sidebar_frame, text="Tasks", style="Sidebar.TButton", command=self._toggle_tasks_submenu)
        tasks_button.pack(pady=(0,5), fill=tk.X, padx=10)

        self.tasks_submenu_frame = tk.Frame(self.sidebar_frame, bg=self.colors["sidebar_button_active_bg"])
        view_tasks_btn = ttk.Button(self.tasks_submenu_frame, text="View Tasks", command=self._show_view_tasks, style="Sidebar.TButton")
        view_tasks_btn.pack(fill=tk.X, pady=2, padx=15)
        add_task_btn = ttk.Button(self.tasks_submenu_frame, text="Add Task", command=self._open_add_task_dialog, style="Sidebar.TButton")
        add_task_btn.pack(fill=tk.X, pady=2, padx=15)
        self.tasks_submenu_visible = False

        categories_button = ttk.Button(self.sidebar_frame, text="Categories", style="Sidebar.TButton", command=self._toggle_categories_submenu)
        categories_button.pack(pady=(0,5), fill=tk.X, padx=10)

        self.categories_submenu_frame = tk.Frame(self.sidebar_frame, bg=self.colors["sidebar_button_active_bg"])
        manage_cat_btn = ttk.Button(self.categories_submenu_frame, text="Manage Categories", command=self._show_manage_categories_view, style="Sidebar.TButton")
        manage_cat_btn.pack(fill=tk.X, pady=2, padx=15)
        add_cat_btn = ttk.Button(self.categories_submenu_frame, text="Add New Category", command=self._open_add_category_dialog, style="Sidebar.TButton")
        add_cat_btn.pack(fill=tk.X, pady=2, padx=15)
        self.categories_submenu_visible = False

        account_button = ttk.Button(self.sidebar_frame, text="Account", style="Sidebar.TButton", command=self._toggle_account_submenu)
        account_button.pack(pady=(0,5), fill=tk.X, padx=10)

        self.account_submenu_frame = tk.Frame(self.sidebar_frame, bg=self.colors["sidebar_button_active_bg"])
        edit_profile_btn = ttk.Button(self.account_submenu_frame, text="Edit Profile", command=self._open_edit_profile_dialog, style="Sidebar.TButton")
        edit_profile_btn.pack(fill=tk.X, pady=2, padx=15)
        logout_btn = ttk.Button(self.account_submenu_frame, text="Logout", command=self._logout, style="Sidebar.TButton")
        logout_btn.pack(fill=tk.X, pady=2, padx=15)
        self.account_submenu_visible = False

        reports_button = ttk.Button(self.sidebar_frame, text="Reports", style="Sidebar.TButton", command=self._show_reports_view)
        reports_button.pack(pady=(0,5), fill=tk.X, padx=10)

        # Theme Toggle Button
        self.theme_toggle_button = ttk.Button(self.sidebar_frame, text="Toggle Dark Mode", style="Sidebar.TButton", command=self._toggle_theme)
        self.theme_toggle_button.pack(side=tk.BOTTOM, pady=10, fill=tk.X, padx=10)


    def _toggle_tasks_submenu(self):
        if self.tasks_submenu_visible:
            self.tasks_submenu_frame.pack_forget()
        else:
            # Find position relative to Tasks button to pack submenu below it
            # This is a bit tricky, might need to adjust if other buttons are dynamic
            # For now, just pack it
            self.tasks_submenu_frame.pack(fill=tk.X, padx=10, pady=(0,5)) # TODO: Position relative to button
        self.tasks_submenu_visible = not self.tasks_submenu_visible

    def _toggle_categories_submenu(self):
        if self.categories_submenu_visible:
            self.categories_submenu_frame.pack_forget()
        else:
            # TODO: Position relative to Categories button. For now, simple pack.
            self.categories_submenu_frame.pack(fill=tk.X, padx=10, pady=(0,5))
        self.categories_submenu_visible = not self.categories_submenu_visible

    def _toggle_account_submenu(self):
        if self.account_submenu_visible:
            self.account_submenu_frame.pack_forget()
        else:
            self.account_submenu_frame.pack(fill=tk.X, padx=10, pady=(0,5))
        self.account_submenu_visible = not self.account_submenu_visible

    def _show_placeholder_view(self, view_name):
        self._clear_content_frame() # Clear before showing placeholder
        label = tk.Label(self.content_frame, text=f"{view_name} View - Coming Soon!",
                         font=('Helvetica', 18),
                         bg=self.colors["content_bg"], fg=self.colors["text_color"])
        label.pack(padx=20, pady=20, expand=True)
        # No return actual_command needed if called directly

    def _clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def _show_view_tasks(self): # Needs to re-apply theme to its created widgets
        self._clear_content_frame()

        if not hasattr(self, 'current_sort_by'):
            self.current_sort_by = "id"
            self.current_sort_order = "DESC"
        if not hasattr(self, 'current_filters'):
            self.current_filters = {}

        # --- Top Controls Frame (Add Task) ---
        top_controls_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        top_controls_frame.pack(pady=(10,0), padx=10, fill=tk.X)

        add_task_main_btn = ttk.Button(top_controls_frame, text="Add New Task", command=self._open_add_task_dialog)
        add_task_main_btn.pack(side=tk.LEFT, padx=(0,10))

        # --- Search Frame ---
        search_frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=(0,5,0,0))
        search_frame.pack(fill=tk.X, padx=10)

        search_label = ttk.Label(search_frame, text="Search:", background=self.colors["content_bg"], foreground=self.colors["label_fg"])
        search_label.pack(side=tk.LEFT, padx=(0,5))
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0,10))
        self.search_entry.bind("<Return>", self._perform_search) # Allow Enter to search

        search_button = ttk.Button(search_frame, text="Search", command=self._perform_search)
        search_button.pack(side=tk.LEFT, padx=(0,5))
        clear_search_button = ttk.Button(search_frame, text="Clear Search", command=self._clear_search)
        clear_search_button.pack(side=tk.LEFT)


        # --- Filter Controls Frame ---
        filter_frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=(0, 5, 0, 0))
        filter_frame.pack(fill=tk.X, padx=10)

        filter_label = ttk.Label(filter_frame, text="Filter by:", background=self.colors["content_bg"], foreground=self.colors["label_fg"])
        filter_label.pack(side=tk.LEFT, padx=(0,5))

        status_label = ttk.Label(filter_frame, text="Status:", background=self.colors["content_bg"], foreground=self.colors["label_fg"])
        status_label.pack(side=tk.LEFT, padx=(5,0))
        self.status_filter_var = tk.StringVar(value="All")
        status_options = ["All", "Pending", "Completed"]
        status_filter_combo = ttk.Combobox(filter_frame, textvariable=self.status_filter_var, values=status_options, width=10, state="readonly")
        status_filter_combo.pack(side=tk.LEFT, padx=(0,10))

        priority_label = ttk.Label(filter_frame, text="Priority:", background=self.colors["content_bg"], foreground=self.colors["label_fg"])
        priority_label.pack(side=tk.LEFT, padx=(5,0))
        self.priority_filter_var = tk.StringVar(value="All")
        priority_options = ["All", "Low", "Medium", "High"]
        priority_filter_combo = ttk.Combobox(filter_frame, textvariable=self.priority_filter_var, values=priority_options, width=10, state="readonly")
        priority_filter_combo.pack(side=tk.LEFT, padx=(0,10))

        category_label = ttk.Label(filter_frame, text="Category:", background=self.colors["content_bg"], foreground=self.colors["label_fg"])
        category_label.pack(side=tk.LEFT, padx=(5,0))
        self.category_filter_var = tk.StringVar(value="All Categories")
        self.category_filter_combobox = ttk.Combobox(filter_frame, textvariable=self.category_filter_var, width=20, state="readonly")
        self._populate_category_filter_combobox()
        self.category_filter_combobox.pack(side=tk.LEFT, padx=(0,10))

        apply_filters_btn = ttk.Button(filter_frame, text="Apply Filters", command=self._apply_filters)
        apply_filters_btn.pack(side=tk.LEFT, padx=10)

        clear_filters_btn = ttk.Button(filter_frame, text="Clear Filters", command=self._clear_filters)
        clear_filters_btn.pack(side=tk.LEFT)

        # --- Task Action Buttons Frame ---
        task_actions_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        task_actions_frame.pack(pady=(5,5), padx=10, fill=tk.X)

        edit_task_btn = ttk.Button(task_actions_frame, text="Edit Selected", command=self._handle_edit_task)
        edit_task_btn.pack(side=tk.LEFT, padx=(0,5))
        delete_task_btn = ttk.Button(controls_frame, text="Delete Selected", command=self._handle_delete_task)
        delete_task_btn.pack(side=tk.LEFT, padx=(0,5))
        mark_done_btn = ttk.Button(controls_frame, text="Mark Done", command=self._handle_mark_task_done)
        mark_done_btn.pack(side=tk.LEFT, padx=(0,5))
        mark_undone_btn = ttk.Button(controls_frame, text="Mark Undone", command=self._handle_mark_task_undone)
        mark_undone_btn.pack(side=tk.LEFT, padx=(0,5))

        # Treeview for tasks
        columns = ("id", "title", "status", "due_date", "priority", "category", "parent_id", "recurring_type", "recurring_end")
        self.task_tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", style="Treeview")

        for col in columns:
            self.task_tree.heading(col, text=col.replace("_", " ").title())
            if col == "id":
                self.task_tree.column(col, width=30, stretch=tk.NO)
            elif col == "title":
                self.task_tree.column(col, width=300)
            elif col == "status":
                 self.task_tree.column(col, width=80, anchor=tk.CENTER)
            else:
                self.task_tree.column(col, width=100, anchor=tk.CENTER)

        # Hide some columns for now, make them sortable by db_col name
        self.task_tree_columns = {
            "id": {"text": "ID", "width": 30, "stretch": tk.NO, "db_col": "id"},
            "title": {"text": "Title", "width": 300, "db_col": "title"},
            "status": {"text": "Status", "width": 80, "anchor": tk.CENTER, "db_col": "completed"}, # Sort by 'completed'
            "due_date": {"text": "Due Date", "width": 100, "anchor": tk.CENTER, "db_col": "due_date"},
            "priority": {"text": "Priority", "width": 100, "anchor": tk.CENTER, "db_col": "priority"},
            "category": {"text": "Category", "width": 100, "anchor": tk.CENTER, "db_col": "category_id"}, # Sort by category_id
             # Hidden columns
            "parent_id": {"text": "Parent ID", "width": 0, "stretch": tk.NO, "db_col": "parent_task_id"},
            "recurring_type": {"text": "Recurring", "width": 0, "stretch": tk.NO, "db_col": "recurring_type"},
            "recurring_end": {"text": "Recur End", "width": 0, "stretch": tk.NO, "db_col": "recurring_end_date"}
        }

        for col_id, col_data in self.task_tree_columns.items():
            self.task_tree.heading(col_id, text=col_data["text"], command=lambda c=col_data["db_col"]: self._sort_tasks_by_column(c))
            self.task_tree.column(col_id, width=col_data["width"], stretch=col_data.get("stretch", tk.YES), anchor=col_data.get("anchor", tk.W))

        # Scrollbar for Treeview
        tree_scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=tree_scrollbar.set)

        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0,10)) # Adjusted padding
        self.task_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))

        self._load_tasks() # Initial load with default sort/filter


    def _parse_due_date(self, raw_due_date): # Keep this utility
        if raw_due_date is None:
            return "" # Return empty string for Treeview if no date
        if isinstance(raw_due_date, datetime): # Should be date object from DB
            return raw_due_date.strftime("%Y-%m-%d")
        if isinstance(raw_due_date, str): # Can be date object from tkcalendar or string from DB
            if hasattr(raw_due_date, 'strftime'): # If it's a date object from tkcalendar
                 return raw_due_date.strftime("%Y-%m-%d")
            try:
                # Assuming DB returns string in "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"
                return datetime.strptime(raw_due_date.split()[0], "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                return raw_due_date # Or handle error
        return str(raw_due_date)


    def _load_tasks(self): # Removed parameters, will use instance variables
        if not hasattr(self, 'task_tree'): return
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        # Use instance variables for current sort, filter, and search states
        order_by_clause = f"{self.current_sort_by} {self.current_sort_order}" if self.current_sort_by else None

        self.tasks_data = self.controller.get_tasks(
            order_by=order_by_clause,
            filter_criteria=self.current_filters,
            search_term=self.current_search_term # Pass search term
        )

        # Update visual indicator for sorting
        for col_id, col_data in self.task_tree_columns.items():
            header_text = col_data["text"]
            # Make sure final_sort_by is not None before comparison
            if final_sort_by and col_data["db_col"] == final_sort_by:
                header_text += " ▲" if final_sort_order == "ASC" else " ▼"
            self.task_tree.heading(col_id, text=header_text)

        # Build a tree structure from the flat list
        tasks_by_id = {task['id']: task for task in self.tasks_data}
        # Initialize children lists for all tasks
        for task_id in tasks_by_id:
            tasks_by_id[task_id]['children_items'] = []

        root_tasks = []
        for task_id, task in tasks_by_id.items():
            parent_id = task.get("parent_task_id")
            if parent_id and parent_id in tasks_by_id:
                tasks_by_id[parent_id]['children_items'].append(task)
            else:
                root_tasks.append(task)

        # Recursive function to insert tasks
        def insert_task_recursively(task_list, parent_tree_id=""):
            for task in task_list:
                status = "Done" if task.get("completed") else "Pending"
                due_date_str = self._parse_due_date(task.get("due_date"))

                category_id = task.get("category_id")
                category_display = self.category_id_to_name_map.get(category_id, "") if category_id else ""


                values = (
                    task.get("id"),
                    task.get("title"),
                    status,
                    due_date_str,
                    task.get("priority", "Medium"),
                    category_display, # Use mapped name
                    task.get("parent_task_id", ""), # This column is hidden, but data is there
                    task.get("recurring_type", ""),
                    self._parse_due_date(task.get("recurring_end_date"))
                )
                # Use task['id'] as the item ID in the treeview (iid)
                # This makes it easy to reference tree items by their actual task ID
                item_id = task['id']
                self.task_tree.insert(parent_tree_id, tk.END, iid=item_id, values=values, open=True) # 'open=True' to expand by default

                # If this task has children, insert them recursively
                if task['children_items']:
                    insert_task_recursively(task['children_items'], parent_tree_id=item_id)

        insert_task_recursively(root_tasks)


    def _open_add_task_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Task")
        dialog.geometry("450x550") # Adjusted size
        dialog.resizable(False, False)
        dialog.transient(self.root) # Keep dialog on top
        dialog.grab_set() # Modal behavior

        frame = ttk.Frame(dialog, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        # Title
        ttk.Label(frame, text="Title:").grid(row=0, column=0, sticky="w", pady=5)
        title_entry = ttk.Entry(frame, width=40)
        title_entry.grid(row=0, column=1, pady=5, sticky="ew")

        # Due Date
        ttk.Label(frame, text="Due Date:").grid(row=1, column=0, sticky="w", pady=5)
        due_date_entry = DateEntry(frame, width=38, date_pattern='yyyy-mm-dd', background='darkblue', foreground='white', borderwidth=2)
        due_date_entry.grid(row=1, column=1, pady=5, sticky="ew")
        # Allow clearing DateEntry by setting its value to empty string
        due_date_entry._set_text("") # Clears the entry initially

        # Priority
        ttk.Label(frame, text="Priority:").grid(row=2, column=0, sticky="w", pady=5)
        priority_var = tk.StringVar(value='Medium')
        priority_options = ['Low', 'Medium', 'High']
        priority_menu = ttk.Combobox(frame, textvariable=priority_var, values=priority_options, width=37, state="readonly")
        priority_menu.grid(row=2, column=1, pady=5, sticky="ew")

        # Category Combobox
        ttk.Label(frame, text="Category:").grid(row=3, column=0, sticky="w", pady=5)
        self.add_task_category_combobox = ttk.Combobox(frame, width=37, state="readonly")
        self.add_task_category_combobox.grid(row=3, column=1, pady=5, sticky="ew")
        self._populate_category_combobox(self.add_task_category_combobox) # Populate it

        # Parent Task ID (manual input)
        ttk.Label(frame, text="Parent Task:").grid(row=4, column=0, sticky="w", pady=5)
        # Store the combobox and mapping for later retrieval of ID
        self.add_task_parent_task_combobox = ttk.Combobox(frame, width=37, state="readonly")
        self.add_task_parent_task_combobox.grid(row=4, column=1, pady=5, sticky="ew")
        self._populate_parent_task_combobox(self.add_task_parent_task_combobox) # Populate it

        # Recurring Type
        ttk.Label(frame, text="Recurring:").grid(row=5, column=0, sticky="w", pady=5)
        recurring_type_var = tk.StringVar(value='None')
        recurring_options = ['None', 'Daily', 'Weekly', 'Monthly'] # Add 'Yearly' if supported by DB
        recurring_type_menu = ttk.Combobox(frame, textvariable=recurring_type_var, values=recurring_options, width=37, state="readonly")
        recurring_type_menu.grid(row=5, column=1, pady=5, sticky="ew")

        # Recurring End Date
        ttk.Label(frame, text="Recurring End Date:").grid(row=6, column=0, sticky="w", pady=5)
        recurring_end_date_entry = DateEntry(frame, width=38, date_pattern='yyyy-mm-dd', background='darkblue', foreground='white', borderwidth=2)
        recurring_end_date_entry.grid(row=6, column=1, pady=5, sticky="ew")
        recurring_end_date_entry._set_text("") # Clears the entry initially

        # Buttons Frame
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=7, column=0, columnspan=2, pady=20)

        def on_save():
            selected_category_name = self.add_task_category_combobox.get()
            category_id_val = self.category_name_to_id_map.get(selected_category_name)

            selected_parent_task_title = self.add_task_parent_task_combobox.get()
            parent_task_id_val = self.parent_task_title_to_id_map.get(selected_parent_task_title)


            self.add_task_action(
                dialog,
                title_entry.get(),
                due_date_entry.get_date() if due_date_entry.get() else None,
                priority_var.get(),
                category_id_val,
                parent_task_id_val, # Pass ID from combobox
                recurring_type_var.get(),
                recurring_end_date_entry.get_date() if recurring_end_date_entry.get() else None
            )

        save_button = ttk.Button(buttons_frame, text="Save Task", command=on_save)
        save_button.pack(side=tk.LEFT, padx=10)

        cancel_button = ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy)
        cancel_button.pack(side=tk.LEFT, padx=10)

        frame.grid_columnconfigure(1, weight=1) # Make entry widgets expand


    def add_task_action(self, dialog, title, due_date, priority, category_id, parent_task_id, recurring_type, recurring_end_date):
        title = title.strip()
        if not title:
            messagebox.showerror("Input Error", "Task title cannot be empty.", parent=dialog)
            return

        # Convert DateEntry objects to "YYYY-MM-DD" strings or None
        due_date_str = due_date.strftime("%Y-%m-%d") if due_date else None
        recurring_end_date_str = recurring_end_date.strftime("%Y-%m-%d") if recurring_end_date else None

        # Handle optional integer fields
        # category_id_val and parent_task_id_val are already IDs or None from combobox handling

        # Handle 'None' string for recurring type
        recurring_type_val = None if recurring_type == 'None' else recurring_type

        try:
            self.controller.add_task(
                title=title,
                user_id=self.user_id, # Use stored user_id
                due_date=due_date_str,
                priority=priority,
                category_id=category_id_val,
                parent_task_id=parent_task_id_val,
                recurring_type=recurring_type_val,
                recurring_end_date=recurring_end_date_str
            )
            messagebox.showinfo("Success", "Task added successfully!", parent=dialog)
            self._load_tasks()  # Refresh the task list in the main window
            dialog.destroy()
        except ValueError as ve: # Catch validation errors from controller/DB layer
            messagebox.showerror("Validation Error", str(ve), parent=dialog)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add task: {e}", parent=dialog)


    # def _toggle_due_date(self): # Old method, remove or adapt for dialog
    #     pass

    # def add_task(self): # Old method, replaced by _open_add_task_dialog and add_task_action
    #     pass

    # def delete_task(self): # To be refactored for Treeview
    #     pass

    # def edit_task(self): # To be refactored for Treeview
    #     pass

    # def mark_done(self): # To be refactored for Treeview
    #     pass

    # --- Category GUI Methods ---

    def _open_add_category_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Category")
        dialog.geometry("350x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text="Category Name:").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = ttk.Entry(frame, width=30)
        name_entry.grid(row=0, column=1, pady=5, sticky="ew")

        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=1, column=0, columnspan=2, pady=20)

        def on_save():
            self._add_category_action(dialog, name_entry.get())

        save_button = ttk.Button(buttons_frame, text="Save Category", command=on_save)
        save_button.pack(side=tk.LEFT, padx=10)
        cancel_button = ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy)
        cancel_button.pack(side=tk.LEFT, padx=10)

        frame.grid_columnconfigure(1, weight=1)
        name_entry.focus()


    def _add_category_action(self, dialog, name):
        name = name.strip()
        if not name:
            messagebox.showerror("Input Error", "Category name cannot be empty.", parent=dialog)
            return

        try:
            self.controller.add_category(name, self.user_id)
            messagebox.showinfo("Success", f"Category '{name}' added successfully!", parent=dialog)
            if hasattr(self, 'category_tree') and self.category_tree.winfo_exists(): # Check if manage view is visible
                 self._load_categories() # Refresh category list if visible
            dialog.destroy()
        except ValueError as ve: # Catch validation errors (e.g., duplicate)
            messagebox.showerror("Validation Error", str(ve), parent=dialog)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add category: {e}", parent=dialog)

    def _show_manage_categories_view(self):
        self._clear_content_frame()

        action_bar = ttk.Frame(self.content_frame, style="Content.TFrame") # Assuming Content.TFrame style exists or default
        action_bar.pack(fill=tk.X, pady=(10,0), padx=10)

        add_button = ttk.Button(action_bar, text="Add New Category", command=self._open_add_category_dialog)
        add_button.pack(side=tk.LEFT, padx=(0,10))

        edit_button = ttk.Button(action_bar, text="Edit Selected", command=self._handle_edit_category)
        edit_button.pack(side=tk.LEFT, padx=(0,10))

        delete_button = ttk.Button(action_bar, text="Delete Selected", command=self._handle_delete_category)
        delete_button.pack(side=tk.LEFT)

        columns = ("id", "name")
        self.category_tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", style="Treeview")
        self.category_tree.heading("id", text="ID")
        self.category_tree.heading("name", text="Category Name")
        self.category_tree.column("id", width=50, stretch=tk.NO, anchor=tk.CENTER)
        self.category_tree.column("name", width=300)

        # Scrollbar
        tree_scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.category_tree.yview)
        self.category_tree.configure(yscrollcommand=tree_scrollbar.set)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0,10), padx=(0,10))
        self.category_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._load_categories()

    def _load_categories(self):
        if not hasattr(self, 'category_tree'): return
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)

        categories = self.controller.fetch_categories(self.user_id)
        if categories:
            for category in categories:
                self.category_tree.insert("", tk.END, values=(category["id"], category["name"]))

    def _handle_edit_category(self):
        selected_item = self.category_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a category to edit.", parent=self.root)
            return
        item_values = self.category_tree.item(selected_item, "values")
        category_id = item_values[0]
        current_name = item_values[1]
        self._open_edit_category_dialog(category_id, current_name)

    def _open_edit_category_dialog(self, category_id, current_name):
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Category")
        dialog.geometry("350x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text="Category Name:").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = ttk.Entry(frame, width=30)
        name_entry.insert(0, current_name)
        name_entry.grid(row=0, column=1, pady=5, sticky="ew")

        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=1, column=0, columnspan=2, pady=20)

        def on_save():
            self._edit_category_action(dialog, category_id, name_entry.get())

        save_button = ttk.Button(buttons_frame, text="Save Changes", command=on_save)
        save_button.pack(side=tk.LEFT, padx=10)
        cancel_button = ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy)
        cancel_button.pack(side=tk.LEFT, padx=10)

        frame.grid_columnconfigure(1, weight=1)
        name_entry.focus()

    def _edit_category_action(self, dialog, category_id, new_name):
        new_name = new_name.strip()
        if not new_name:
            messagebox.showerror("Input Error", "Category name cannot be empty.", parent=dialog)
            return
        try:
            self.controller.update_category(category_id, self.user_id, new_name)
            messagebox.showinfo("Success", "Category updated successfully!", parent=dialog)
            self._load_categories()
            dialog.destroy()
        except ValueError as ve:
            messagebox.showerror("Validation Error", str(ve), parent=dialog)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update category: {e}", parent=dialog)

    def _handle_delete_category(self):
        selected_item = self.category_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a category to delete.", parent=self.root)
            return
        item_values = self.category_tree.item(selected_item, "values")
        category_id = item_values[0]
        category_name = item_values[1]

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete category '{category_name}'?\nThis might affect tasks associated with this category.", parent=self.root)
        if confirm:
            self._delete_category_action(category_id)

    def _delete_category_action(self, category_id):
        try:
            self.controller.delete_category(category_id, self.user_id)
            messagebox.showinfo("Success", "Category deleted successfully!", parent=self.root)
            self._load_categories()
        except Exception as e:
            # Catching general exception as DB layer might raise IntegrityError if category is in use and FK constraint is RESTRICT
            messagebox.showerror("Error", f"Failed to delete category: {e}\nIt might be in use by some tasks.", parent=self.root)

    def _populate_category_combobox(self, combobox_widget, current_category_id=None, add_all_option=False):
        categories = self.controller.fetch_categories(self.user_id)

        # Ensure maps are initialized even if no categories
        if not hasattr(self, 'category_name_to_id_map'):
            self.category_name_to_id_map = {}
        if not hasattr(self, 'category_id_to_name_map'):
            self.category_id_to_name_map = {}

        self.category_name_to_id_map.clear()
        self.category_id_to_name_map.clear()

        for cat in categories:
            self.category_name_to_id_map[cat["name"]] = cat["id"]
            self.category_id_to_name_map[cat["id"]] = cat["name"]

        category_names = sorted(list(self.category_name_to_id_map.keys()))

        if add_all_option:
            combobox_values = ["All Categories"] + category_names
            combobox_widget.set("All Categories")
        else:
            combobox_values = [""] + category_names # Blank for "no category"
            if current_category_id and current_category_id in self.category_id_to_name_map:
                combobox_widget.set(self.category_id_to_name_map[current_category_id])
            else:
                combobox_widget.set("")

        combobox_widget['values'] = combobox_values


    def _populate_category_filter_combobox(self):
        if hasattr(self, 'category_filter_combobox'):
            self._populate_category_combobox(self.category_filter_combobox, add_all_option=True)


    # --- Task Edit/Delete/Mark Methods ---
    def _get_selected_task_id(self):
        selected_item = self.task_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a task first.", parent=self.root)
            return None
        item_values = self.task_tree.item(selected_item, "values")
        return item_values[0] # ID is the first column

    def _handle_edit_task(self):
        task_id = self._get_selected_task_id()
        if not task_id: return

        try:
            task_data = self.controller.get_task_by_id(task_id, self.user_id)
            if task_data:
                self._open_edit_task_dialog(task_data)
            else:
                messagebox.showerror("Error", "Task not found or access denied.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch task details: {e}", parent=self.root)

    def _open_edit_task_dialog(self, task_data):
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Task")
        dialog.geometry("450x600") # Slightly taller for completed status
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        # Field setup (similar to add dialog, but pre-filled)
        # Title
        ttk.Label(frame, text="Title:").grid(row=0, column=0, sticky="w", pady=5)
        title_entry = ttk.Entry(frame, width=40)
        title_entry.insert(0, task_data.get("title", ""))
        title_entry.grid(row=0, column=1, pady=5, sticky="ew")

        # Due Date
        ttk.Label(frame, text="Due Date:").grid(row=1, column=0, sticky="w", pady=5)
        due_date_entry = DateEntry(frame, width=38, date_pattern='yyyy-mm-dd')
        due_date_val = task_data.get("due_date")
        if due_date_val:
            if isinstance(due_date_val, str):
                try: due_date_entry.set_date(datetime.strptime(due_date_val, "%Y-%m-%d"))
                except: pass # Keep blank if parse fails
            elif isinstance(due_date_val, datetime.date) or isinstance(due_date_val, datetime):
                 due_date_entry.set_date(due_date_val)
            else:
                 due_date_entry._set_text("")
        else:
            due_date_entry._set_text("")
        due_date_entry.grid(row=1, column=1, pady=5, sticky="ew")

        # Priority
        ttk.Label(frame, text="Priority:").grid(row=2, column=0, sticky="w", pady=5)
        priority_var = tk.StringVar(value=task_data.get("priority", 'Medium'))
        priority_options = ['Low', 'Medium', 'High']
        priority_menu = ttk.Combobox(frame, textvariable=priority_var, values=priority_options, width=37, state="readonly")
        priority_menu.grid(row=2, column=1, pady=5, sticky="ew")

        # Category
        ttk.Label(frame, text="Category:").grid(row=3, column=0, sticky="w", pady=5)
        edit_task_category_combobox = ttk.Combobox(frame, width=37, state="readonly")
        edit_task_category_combobox.grid(row=3, column=1, pady=5, sticky="ew")
        self._populate_category_combobox(edit_task_category_combobox, task_data.get("category_id"))

        # Parent Task ID
        ttk.Label(frame, text="Parent Task:").grid(row=4, column=0, sticky="w", pady=5)
        edit_task_parent_task_combobox = ttk.Combobox(frame, width=37, state="readonly")
        edit_task_parent_task_combobox.grid(row=4, column=1, pady=5, sticky="ew")
        self._populate_parent_task_combobox(edit_task_parent_task_combobox,
                                           current_parent_id=task_data.get("parent_task_id"),
                                           exclude_task_id=task_data.get("id"))


        # Recurring Type
        ttk.Label(frame, text="Recurring:").grid(row=5, column=0, sticky="w", pady=5)
        recurring_type_var = tk.StringVar(value=task_data.get("recurring_type") or 'None')
        recurring_options = ['None', 'Daily', 'Weekly', 'Monthly']
        recurring_type_menu = ttk.Combobox(frame, textvariable=recurring_type_var, values=recurring_options, width=37, state="readonly")
        recurring_type_menu.grid(row=5, column=1, pady=5, sticky="ew")

        # Recurring End Date
        ttk.Label(frame, text="Recurring End:").grid(row=6, column=0, sticky="w", pady=5)
        recurring_end_date_entry = DateEntry(frame, width=38, date_pattern='yyyy-mm-dd')
        rec_end_date_val = task_data.get("recurring_end_date")
        if rec_end_date_val:
            if isinstance(rec_end_date_val, str):
                try: recurring_end_date_entry.set_date(datetime.strptime(rec_end_date_val, "%Y-%m-%d"))
                except: pass
            elif isinstance(rec_end_date_val, datetime.date) or isinstance(rec_end_date_val, datetime):
                 recurring_end_date_entry.set_date(rec_end_date_val)
            else: # Clear if not valid
                recurring_end_date_entry._set_text("")
        else: # Clear if None
            recurring_end_date_entry._set_text("")
        recurring_end_date_entry.grid(row=6, column=1, pady=5, sticky="ew")

        # Completed Status
        ttk.Label(frame, text="Completed:").grid(row=7, column=0, sticky="w", pady=5)
        completed_var = tk.BooleanVar(value=bool(task_data.get("completed", False)))
        completed_check = ttk.Checkbutton(frame, variable=completed_var)
        completed_check.grid(row=7, column=1, pady=5, sticky="w")

        # Buttons
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=8, column=0, columnspan=2, pady=20)

        def on_save():
            selected_category_name = edit_task_category_combobox.get()
            category_id_val = self.category_name_to_id_map.get(selected_category_name)

            selected_parent_task_title = edit_task_parent_task_combobox.get()
            parent_task_id_val = self.parent_task_title_to_id_map.get(selected_parent_task_title)

            updated_data = {
                "new_title": title_entry.get(),
                "new_due_date": due_date_entry.get_date() if due_date_entry.get() else None,
                "new_priority": priority_var.get(),
                "new_category_id": category_id_val,
                "new_parent_task_id": parent_task_id_val, # From combobox
                "new_recurring_type": recurring_type_var.get(),
                "new_recurring_end_date": recurring_end_date_entry.get_date() if recurring_end_date_entry.get() else None,
                "new_completed_status": completed_var.get()
            }
            self._edit_task_action(dialog, task_data["id"], updated_data)

        save_button = ttk.Button(buttons_frame, text="Save Changes", command=on_save)
        save_button.pack(side=tk.LEFT, padx=10)
        cancel_button = ttk.Button(buttons_frame, text="Cancel", command=dialog.destroy)
        cancel_button.pack(side=tk.LEFT, padx=10)
        frame.grid_columnconfigure(1, weight=1)

    def _edit_task_action(self, dialog, task_id, updated_data):
        title = updated_data["new_title"].strip()
        if not title:
            messagebox.showerror("Input Error", "Task title cannot be empty.", parent=dialog)
            return

        # Convert dates and optional IDs
        due_date_str = updated_data["new_due_date"].strftime("%Y-%m-%d") if updated_data["new_due_date"] else None
        rec_end_date_str = updated_data["new_recurring_end_date"].strftime("%Y-%m-%d") if updated_data["new_recurring_end_date"] else None

        # parent_task_id is already an ID or None from combobox handling in updated_data
        parent_id_val = updated_data["new_parent_task_id"]

        recurring_type_val = None if updated_data["new_recurring_type"] == 'None' else updated_data["new_recurring_type"]

        try:
            self.controller.update_task(
                task_id=task_id,
                new_title=title,
                new_due_date=due_date_str,
                new_priority=updated_data["new_priority"],
                new_category_id=updated_data["new_category_id"], # Already ID or None
                new_parent_task_id=parent_id_val,
                new_recurring_type=recurring_type_val,
                new_recurring_end_date=rec_end_date_str,
                new_completed_status=updated_data["new_completed_status"]
            )
            messagebox.showinfo("Success", "Task updated successfully!", parent=dialog)
            self._load_tasks()
            dialog.destroy()
        except ValueError as ve:
            messagebox.showerror("Validation Error", str(ve), parent=dialog)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update task: {e}", parent=dialog)

    def _handle_delete_task(self):
        task_id = self._get_selected_task_id()
        if not task_id: return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?", parent=self.root)
        if confirm:
            try:
                self.controller.delete_task(task_id) # Assumes controller ensures user owns task or is admin
                messagebox.showinfo("Success", "Task deleted successfully.", parent=self.root)
                self._load_tasks()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete task: {e}", parent=self.root)

    def _handle_mark_task_done(self):
        task_id = self._get_selected_task_id()
        if not task_id: return
        try:
            self.controller.mark_task_status(task_id, True)
            self._load_tasks()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to mark task as done: {e}", parent=self.root)

    def _handle_mark_task_undone(self):
        task_id = self._get_selected_task_id()
        if not task_id: return
        try:
            self.controller.mark_task_status(task_id, False)
            self._load_tasks()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to mark task as undone: {e}", parent=self.root)

    # --- Sorting and Filtering Methods ---
    def _sort_tasks_by_column(self, column_db_name):
        if self.current_sort_by == column_db_name:
            self.current_sort_order = "DESC" if self.current_sort_order == "ASC" else "ASC"
        else:
            self.current_sort_by = column_db_name
            self.current_sort_order = "ASC"

        self._load_tasks() # Reload tasks with new sort order

    def _apply_filters(self):
        filters = {}
        status_filter = self.status_filter_var.get()
        if status_filter == "Completed":
            filters["completed"] = True
        elif status_filter == "Pending":
            filters["completed"] = False
        # "All" means no filter on completed status

        priority_filter = self.priority_filter_var.get()
        if priority_filter != "All":
            filters["priority"] = priority_filter

        category_filter_name = self.category_filter_var.get()
        if category_filter_name != "All Categories" and category_filter_name != "": # Check for empty string too
            category_id = self.category_name_to_id_map.get(category_filter_name)
            if category_id is not None:
                 filters["category_id"] = category_id
            # else: # Category name not found, could log this or ignore
                 # print(f"Warning: Category name '{category_filter_name}' not found in map for filtering.")

        self.current_filters = filters
        self._load_tasks()

    def _clear_filters(self):
        self.status_filter_var.set("All")
        self.priority_filter_var.set("All")
        self.category_filter_var.set("All Categories")
        if hasattr(self, 'category_filter_combobox'):
            self._populate_category_filter_combobox()
        self.current_filters = {}
        # Also clear search when clearing filters for simplicity, or make it separate
        if hasattr(self, 'search_entry'): self.search_entry.delete(0, tk.END)
        self.current_search_term = ""
        self._load_tasks()

    # --- Search Methods ---
    def _perform_search(self, event=None): # event is passed by <Return> binding
        self.current_search_term = self.search_entry.get()
        self._load_tasks()

    def _clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.current_search_term = ""
        self._load_tasks()

    # --- Account and Reports Methods ---
    def _open_edit_profile_dialog(self): # Apply theme to dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("User Profile")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.config(bg=self.colors["dialog_bg"]) # Theme background

        frame = ttk.Frame(dialog, padding="20", style="Content.TFrame") # Use a themed frame if available
        frame.pack(expand=True, fill=tk.BOTH)
        frame.config(style="Content.TFrame") # Ensure style is applied if Content.TFrame bg is from theme

        ttk.Label(frame, text=f"User ID: {self.user_id}", font=('Helvetica', 11), background=self.colors["dialog_bg"], foreground=self.colors["label_fg"]).pack(pady=10)
        ttk.Label(frame, text="Username: [Username Placeholder]", font=('Helvetica', 11), background=self.colors["dialog_bg"], foreground=self.colors["label_fg"]).pack(pady=5)
        ttk.Label(frame, text="Email: [Email Placeholder]", font=('Helvetica', 11), background=self.colors["dialog_bg"], foreground=self.colors["label_fg"]).pack(pady=5)

        close_button = ttk.Button(frame, text="Close", command=dialog.destroy) # Uses TButton style
        close_button.pack(pady=20)
        dialog.focus()

    def _logout(self):
        print(f"User {self.user_id} logging out.")
        self.root.destroy()
        if self.on_logout_callback:
            self.on_logout_callback()

    def _show_reports_view(self):
        self._clear_content_frame()
        label = tk.Label(self.content_frame, text="Reports View - Coming Soon!",
                         font=('Helvetica', 18),
                         bg=self.colors["content_bg"], fg=self.colors["text_color"])
        label.pack(padx=20, pady=20, expand=True)

    # --- Theme Methods ---
    def _toggle_theme(self):
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.theme_toggle_button.config(text="Toggle Light Mode" if self.current_theme == 'dark' else "Toggle Dark Mode")
        self._apply_theme()

    def _apply_theme(self):
        self._configure_styles() # Reconfigure ttk styles with the new theme

        # Update non-ttk widget colors directly
        self.root.config(bg=self.colors["content_bg"])
        self.sidebar_frame.config(bg=self.colors["sidebar_bg"])
        self.menu_label.config(bg=self.colors["sidebar_bg"], fg=self.colors["sidebar_fg"])
        self.content_frame.config(bg=self.colors["content_bg"])

        # Update submenu frame backgrounds (these are tk.Frame)
        self.tasks_submenu_frame.config(bg=self.colors["sidebar_button_active_bg"])
        self.categories_submenu_frame.config(bg=self.colors["sidebar_button_active_bg"])
        self.account_submenu_frame.config(bg=self.colors["sidebar_button_active_bg"])

        # Re-render the current view to apply changes to its internal widgets
        # This is a bit broad; more targeted updates would be better if performance was an issue.
        if hasattr(self, '_show_view_tasks') and self.content_frame.winfo_ismapped(): # Check if task view related widgets exist
            # Determine which view is active and refresh it.
            # For simplicity, just refresh if task_tree exists (implies task view or category view might be active)
            # A more robust way is to track current_view.
            # For now, if task_tree exists, it's likely the tasks view.
            # If category_tree exists, it's the categories view.
            # If reports label exists, it's reports view.

            # This logic is simplified: it just re-calls the method for the most common views
            # to reconstruct them with new theme colors.
            current_children = self.content_frame.winfo_children()
            if any(isinstance(w, ttk.Treeview) for w in current_children): # Heuristic for treeview based views
                 if hasattr(self, 'task_tree') and self.task_tree in current_children:
                    self._show_view_tasks()
                 elif hasattr(self, 'category_tree') and self.category_tree in current_children:
                    self._show_manage_categories_view()
            elif any(c.cget("text") == "Reports View - Coming Soon!" for c in current_children if isinstance(c, tk.Label)):
                 self._show_reports_view()
            # Add other views if they exist e.g. profile, etc.
            # else: # Fallback or if it's a placeholder view
                 # self._show_placeholder_view("Current View") # This needs a way to know current view name


def launch_gui(user_id, on_logout_callback=None):
    root = tk.Tk()
    app = ToDoApp(root, user_id, on_logout_callback=on_logout_callback)
    root.mainloop()
