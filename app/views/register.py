import tkinter as tk
from tkinter import messagebox
import bcrypt
from app.models.database import Database


class RegisterWindow:
    def __init__(self, root, on_register_success=None):
        self.root = root
        self.root.title("Register")
        self.root.geometry("400x300")
        self.on_register_success = on_register_success
        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        # Username
        tk.Label(frame, text="Username:", font=("Arial", 14)).grid(row=0, column=0, sticky="w", pady=(0, 10))
        self.username_entry = tk.Entry(frame, font=("Arial", 14))
        self.username_entry.grid(row=0, column=1, pady=(0, 10))

        # Email
        tk.Label(frame, text="Email:", font=("Arial", 14)).grid(row=1, column=0, sticky="w", pady=(0, 10))
        self.email_entry = tk.Entry(frame, font=("Arial", 14))
        self.email_entry.grid(row=1, column=1, pady=(0, 10))

        # Password
        tk.Label(frame, text="Password:", font=("Arial", 14)).grid(row=2, column=0, sticky="w", pady=(0, 10))
        self.password_entry = tk.Entry(frame, show="*", font=("Arial", 14))
        self.password_entry.grid(row=2, column=1, pady=(0, 10))

        # Confirm Password
        tk.Label(frame, text="Confirm Password:", font=("Arial", 14)).grid(row=3, column=0, sticky="w", pady=(0, 20))
        self.confirm_password_entry = tk.Entry(frame, show="*", font=("Arial", 14))
        self.confirm_password_entry.grid(row=3, column=1, pady=(0, 20))

        # Register Button
        register_btn = tk.Button(frame, text="Register", font=("Arial", 14), command=self.register)
        register_btn.grid(row=4, column=0, columnspan=2, pady=10, ipadx=10, ipady=5)

    def register(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if not username or not email or not password or not confirm_password:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Input Error", "Passwords do not match.")
            return

        db = Database()

        # Check if username or email already exists
        if db.get_user_by_username(username):
            messagebox.showerror("Registration Error", "Username already exists.")
            return
        if db.get_user_by_email(email):
            messagebox.showerror("Registration Error", "Email already exists.")
            return

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            db.register_user(username, email, hashed_password)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to register user: {e}")
            return

        messagebox.showinfo("Success", "Registration successful! You can now log in.")
        self.root.destroy()
        if self.on_register_success:
            self.on_register_success()
