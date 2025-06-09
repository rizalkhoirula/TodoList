# main.py - Application Entry Point

import sys
# Add the 'app' directory to sys.path to allow imports from 'app'
# This might be needed if running main.py directly from the root and Python doesn't find 'app'
# For example, if you get ModuleNotFoundError for 'from app.views.login import launch_login'
# However, if 'app' is a package and main.py is outside, Python should handle it with proper PYTHONPATH or execution from root.
# Let's assume for now that Python's import system can find 'app' if main.py is in the root.
# If not, one might need:
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


# It's better to ensure that the 'app' package and its modules are correctly structured
# and that this script is run from a context where 'app' is discoverable (e.g. root directory).

try:
    from app.views.login import launch_login
    from app.views.gui import launch_gui
except ImportError as e:
    print(f"Import Error: {e}. Ensure you are running from the project root directory,")
    print(f"and that 'app' is discoverable. Current sys.path: {sys.path}")
    sys.exit(1)

main_app_root = None # Global reference to the main app's Tk root

def start_main_application_window(user_id):
    """Launches the main application window."""
    global main_app_root
    # If there was a previous main_app_root, ensure it's destroyed.
    # However, Tkinter handles root window destruction fairly well.
    # launch_gui will create a new Tk() root internally or expect one.
    # For simplicity, launch_gui creates its own root.
    print(f"Main app launching for user_id: {user_id}")
    # To ensure a clean slate if logging out and in again, launch_gui should handle its own root.
    # launch_gui might need to be adjusted if it doesn't create its own Tk() root.
    # The current launch_gui(user_id) in views/gui.py creates its own root = tk.Tk()
    launch_gui(user_id, on_logout_callback=start_login_window)


def start_login_window():
    """Launches the login window."""
    global main_app_root
    # If the main app window exists, destroy it before showing login.
    # This logic is tricky if Tk roots are managed inside launch_gui/launch_login.
    # For now, we assume that destroying a root window in Tkinter also destroys its children.
    # And that new calls to launch_login/gui create fresh windows.
    print("Logout successful or app start, launching login window.")
    launch_login(on_login_success_callback=start_main_application_window)


if __name__ == "__main__":
    print("Application starting...")
    start_login_window()
