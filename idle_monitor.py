import sys
import time
import os
import subprocess
import argparse
import win32api
import win32con
from pathlib import Path
import pythoncom
import win32com.client

def get_idle_time():
    """Get the system idle time in seconds."""
    lastInputInfo = win32api.GetLastInputInfo()
    elapsed = (win32api.GetTickCount() - lastInputInfo) / 1000.0
    return elapsed

def execute_file(file_path):
    """Execute a file based on its extension."""
    try:
        ext = file_path.suffix.lower()
        
        if ext == '.exe':
            subprocess.Popen([str(file_path)])
        
        elif ext == '.bat':
            subprocess.Popen(['cmd', '/c', str(file_path)])
        
        elif ext == '.ps1':
            subprocess.Popen(['powershell', '-ExecutionPolicy', 'Bypass', '-File', str(file_path)])
        
        elif ext == '.lnk':
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(file_path))
            target_path = shortcut.Targetpath
            if target_path:
                subprocess.Popen([target_path])
        
        print(f"Executed: {file_path}")
    except Exception as e:
        print(f"Error executing {file_path}: {str(e)}")

def execute_folder_files(folder_path):
    """Execute all supported files in the specified folder."""
    folder = Path(folder_path)
    folder.mkdir(exist_ok=True)  # Create folder if it doesn't exist

    supported_extensions = {'.exe', '.bat', '.ps1', '.lnk'}
    
    for file_path in folder.glob('*'):
        if file_path.suffix.lower() in supported_extensions:
            execute_file(file_path)

def main():
    parser = argparse.ArgumentParser(description='Monitor system idle state and execute files.')
    parser.add_argument('idle_time', type=int, help='Idle time threshold in seconds')
    args = parser.parse_args()

    # Create required folders at startup
    Path('on_idle').mkdir(exist_ok=True)
    Path('on_idle_end').mkdir(exist_ok=True)

    print(f"Monitoring system idle state (threshold: {args.idle_time} seconds)")
    print("Press Ctrl+C to exit")

    was_idle = False
    
    try:
        while True:
            idle_time = get_idle_time()
            
            # Check if system just became idle
            if not was_idle and idle_time >= args.idle_time:
                print("\nSystem is now idle")
                execute_folder_files('on_idle')
                was_idle = True
            
            # Check if system just became active
            elif was_idle and idle_time < args.idle_time:
                print("\nSystem is now active")
                execute_folder_files('on_idle_end')
                was_idle = False
            
            time.sleep(1)  # Check every second
            
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == '__main__':
    main()
