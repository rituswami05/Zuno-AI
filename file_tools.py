import os
import shutil
import subprocess

# ============================================================
# ZUNO PROJECT DIRECTORY (DEFAULT FALLBACK)
# ============================================================
BASE_PATH = os.getcwd()
PYCHARM_PATH = r"E:\py\PyCharm 2026.2.0.1\bin\pycharm64.exe"

# ============================================================
# SMART PATH RESOLVER
# ============================================================
def resolve_path(name: str) -> str:
    """Automatically maps keywords like 'Downloads' to the correct Windows user folder."""
    # Get your actual Windows user directory (e.g., C:\Users\dheer)
    home_dir = os.path.expanduser("~")
    
    # Normalize slashes just in case
    name = name.replace("\\", "/")
    parts = name.split("/")
    first_part = parts[0].lower()

    # Map friendly names to actual Windows paths
    if "download" in first_part:
        return os.path.join(home_dir, "Downloads", *parts[1:])
    elif "desktop" in first_part:
        return os.path.join(home_dir, "Desktop", *parts[1:])
    elif "document" in first_part:
        return os.path.join(home_dir, "Documents", *parts[1:])
    
    # If it's already an absolute path (C:\...), use it directly
    if os.path.isabs(name):
        return name
        
    # Otherwise, fallback to the default Zuno folder
    return os.path.abspath(os.path.join(BASE_PATH, name))

# ============================================================
# CREATE FOLDER
# ============================================================
def create_folder(folder_name: str) -> str:
    try:
        folder_path = resolve_path(folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return f"SUCCESS: Folder created at {folder_path}."
    except Exception as e:
        return f"ERROR: Could not create folder: {e}"

# ============================================================
# CREATE FILE
# ============================================================
def create_file(file_name: str, content: str = "") -> str:
    try:
        file_path = resolve_path(file_name)
        parent_folder = os.path.dirname(file_path)
        
        if parent_folder:
            os.makedirs(parent_folder, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        return f"SUCCESS: File created at {file_path}."
    except Exception as e:
        return f"ERROR: Could not create file: {e}"

# ============================================================
# OPEN FOLDER IN FILE EXPLORER
# ============================================================
def open_folder(folder_name: str) -> str:
    try:
        folder_path = resolve_path(folder_name)
        if not os.path.isdir(folder_path):
            return f"ERROR: Folder does not exist at {folder_path}."
        os.startfile(folder_path)
        return f"SUCCESS: Folder opened."
    except Exception as e:
        return f"ERROR: Could not open folder: {e}"

# ============================================================
# OPEN FILE / FOLDER IN PYCHARM
# ============================================================
def open_file_in_pycharm(file_name: str) -> str:
    try:
        file_path = resolve_path(file_name)
        if not os.path.isfile(file_path):
            return f"ERROR: File does not exist at {file_path}."
        if not os.path.exists(PYCHARM_PATH):
            return f"ERROR: PyCharm not found at {PYCHARM_PATH}"

        subprocess.Popen([PYCHARM_PATH, file_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        return f"SUCCESS: Opened in PyCharm."
    except Exception as e:
        return f"ERROR: Could not open in PyCharm: {e}"

def open_folder_in_pycharm(folder_name: str) -> str:
    try:
        folder_path = resolve_path(folder_name)
        if not os.path.isdir(folder_path):
            return f"ERROR: Folder does not exist at {folder_path}."
        if not os.path.exists(PYCHARM_PATH):
            return f"ERROR: PyCharm not found at {PYCHARM_PATH}"

        subprocess.Popen([PYCHARM_PATH, folder_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        return f"SUCCESS: Opened folder in PyCharm."
    except Exception as e:
        return f"ERROR: Could not open folder in PyCharm: {e}"

# ============================================================
# RENAME FILE OR FOLDER
# ============================================================
def rename_file(old_name: str, new_name: str) -> str:
    try:
        old_path = resolve_path(old_name)
        new_path = resolve_path(new_name)

        if not os.path.exists(old_path):
            return f"ERROR: '{old_path}' does not exist."
        if os.path.exists(new_path):
            return f"ERROR: '{new_path}' already exists."

        os.rename(old_path, new_path)
        return f"SUCCESS: Renamed file."
    except Exception as e:
        return f"ERROR: Could not rename file: {e}"

# ============================================================
# DELETE FILE OR FOLDER
# ============================================================
def delete_file_or_folder(name: str) -> str:
    try:
        path = resolve_path(name)

        if not os.path.exists(path):
            return f"ERROR: '{path}' does not exist."

        if os.path.isfile(path):
            os.remove(path)
            return f"SUCCESS: File deleted."

        if os.path.isdir(path):
            shutil.rmtree(path)
            return f"SUCCESS: Folder deleted."

        return f"ERROR: Could not determine what '{path}' is."
    except Exception as e:
        return f"ERROR: Could not delete: {e}"

# ============================================================
# CLOSE APPLICATION
# ============================================================
# ============================================================
# CLOSE APPLICATION
# ============================================================
def close_application(app_name: str) -> str:
    """Closes an open application on the computer."""
    try:
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "chrome": "chrome.exe",
            "pycharm": "pycharm64.exe",
            "spotify": "spotify.exe",
            "whatsapp": "whatsapp.exe"
        }
        
        exe_name = apps.get(app_name.lower(), f"{app_name.lower()}.exe")
        
        # Try standard Windows taskkill first. 
        # The /T flag is new - it forces Windows to kill "Child Processes" (required for WhatsApp)
        exit_code = os.system(f"taskkill /IM {exe_name} /F /T")
        
        # If standard taskkill still says "not found", we bring out the heavy artillery:
        # PowerShell will hunt down ANYTHING with "whatsapp" in the name and destroy it.
        if exit_code != 0:
            os.system(f'powershell -Command "Get-Process *{app_name.lower()}* | Stop-Process -Force"')
            
        return f"SUCCESS: Closed {app_name}."
    except Exception as e:
        return f"ERROR: Could not close {app_name}: {e}"