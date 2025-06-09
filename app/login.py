# app/login.py

import tkinter as tk
from tkinter import messagebox
import bcrypt
from app.database import Database
from app.register import RegisterWindow


class LoginWindow:
    def __init__(self, root, on_login_success=None):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self._center_window()
        self._build_ui()

    def _center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')

    def _build_ui(self):
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        title_label = tk.Label(frame, text="Welcome to ToDo App", font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(frame, text="Username:", font=("Arial", 14)).grid(row=1, column=0, sticky="w", pady=(0, 10))
        self.username_entry = tk.Entry(frame, font=("Arial", 14))
        self.username_entry.grid(row=1, column=1, pady=(0, 10))

        tk.Label(frame, text="Password:", font=("Arial", 14)).grid(row=2, column=0, sticky="w", pady=(0, 20))
        self.password_entry = tk.Entry(frame, show="*", font=("Arial", 14))
        self.password_entry.grid(row=2, column=1, pady=(0, 20))

        login_btn = tk.Button(frame, text="Login", font=("Arial", 14), command=self.login)
        login_btn.grid(row=3, column=0, columnspan=2, pady=10, ipadx=10, ipady=5)

        register_btn = tk.Button(frame, text="Register", font=("Arial", 14), command=self.register)
        register_btn.grid(row=4, column=0, columnspan=2, pady=10, ipadx=10, ipady=5)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        db = Database()
        user = db.get_user_by_username(username)

        if user and self.check_password(password, user["password_hash"]):
            messagebox.showinfo("Success", "Login successful!")
            self.root.destroy()
            if self.on_login_success:
                self.on_login_success(user["id"])
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register(self):
        reg_root = tk.Toplevel(self.root)
        RegisterWindow(reg_root)

    def check_password(self, plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def launch_login():
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
