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
import tkinter as tk
from tkinter import scrolledtext
import threading
from datetime import datetime

class IdleMonitorGUI:
    def __init__(self, idle_threshold):
        self.idle_threshold = idle_threshold
        self.was_idle = False
        self.running = True
        
        # Dark theme colors
        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.entry_bg = "#3c3c3c"
        self.button_bg = "#404040"
        self.button_hover = "#505050"
        self.accent_color = "#0078d4"
        self.frame_bg = "#333333"
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Idle Starter Monitor")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        self.root.configure(bg=self.bg_color)
        
        # Create status frame
        status_frame = tk.Frame(self.root, bg=self.frame_bg)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Status label
        self.status_label = tk.Label(status_frame, text="Initializing...", 
                                   font=("Arial", 10, "bold"), 
                                   bg=self.frame_bg, fg=self.fg_color)
        self.status_label.pack(side=tk.LEFT)
        
        # Idle time label
        self.idle_time_label = tk.Label(status_frame, text="Idle: 0s", 
                                      font=("Arial", 9), 
                                      bg=self.frame_bg, fg="#cccccc")
        self.idle_time_label.pack(side=tk.RIGHT)
        
        # Create log text area
        log_frame = tk.Frame(self.root, bg=self.bg_color)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        log_label = tk.Label(log_frame, text="Activity Log:", 
                           font=("Arial", 9), 
                           bg=self.bg_color, fg=self.fg_color)
        log_label.pack(anchor=tk.W)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, width=60, 
                                                font=("Consolas", 9),
                                                bg=self.entry_bg, fg=self.fg_color,
                                                insertbackground=self.fg_color,
                                                selectbackground=self.accent_color,
                                                selectforeground=self.fg_color)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Create button frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Exit button
        exit_button = tk.Button(button_frame, text="Exit", command=self.on_closing, 
                              bg="#dc3545", fg="white", font=("Arial", 9),
                              activebackground="#c82333", activeforeground="white",
                              relief="flat", padx=15, pady=5)
        exit_button.pack(side=tk.RIGHT)
        
        # Clear log button
        clear_button = tk.Button(button_frame, text="Clear Log", command=self.clear_log,
                               bg=self.button_bg, fg=self.fg_color, font=("Arial", 9),
                               activebackground=self.button_hover, activeforeground=self.fg_color,
                               relief="flat", padx=15, pady=5)
        clear_button.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start monitoring in a separate thread
        self.monitor_thread = threading.Thread(target=self.monitor_idle_state, daemon=True)
        self.monitor_thread.start()
        
        # Start GUI update timer
        self.update_gui()
        
    def log_message(self, message):
        """Add a timestamped message to the log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        # Thread-safe GUI update
        self.root.after(0, self._update_log_text, formatted_message)
    
    def _update_log_text(self, message):
        """Update the log text widget (must be called from main thread)."""
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
    
    def clear_log(self):
        """Clear the log text area."""
        self.log_text.delete(1.0, tk.END)
    
    def update_status(self, status, idle_time):
        """Update the status labels."""
        def _update():
            self.status_label.config(text=status)
            self.idle_time_label.config(text=f"Idle: {int(idle_time)} / {self.idle_threshold}")
            
            # Color coding for status (dark theme friendly colors)
            if "Monitoring" in status:
                self.status_label.config(fg="#5dade2")  # Light blue
            elif "IDLE" in status:
                self.status_label.config(fg="#f39c12")  # Orange
            elif "ACTIVE" in status:
                self.status_label.config(fg="#58d68d")  # Light green
        
        self.root.after(0, _update)
    
    def update_gui(self):
        """Periodic GUI updates."""
        if self.running:
            self.root.after(1000, self.update_gui)  # Update every second
    
    def on_closing(self):
        """Handle window closing."""
        self.running = False
        self.log_message("Shutting down...")
        self.root.after(100, self.root.destroy)  # Give time for the log message
    
    def monitor_idle_state(self):
        """Monitor the system idle state (runs in background thread)."""
        self.log_message(f"Started monitoring (threshold: {self.idle_threshold} seconds)")
        
        while self.running:
            try:
                idle_time = get_idle_time()
                
                if not self.was_idle:
                    self.update_status("Monitoring - System Active", idle_time)
                    # Wait for the full threshold before considering system idle
                    if idle_time >= self.idle_threshold:
                        self.update_status("System is IDLE", idle_time)
                        self.log_message("System is now idle")
                        execute_folder_files('on_idle', self.log_message)
                        self.was_idle = True
                else:
                    self.update_status("System is IDLE", idle_time)
                    # When system is idle, check every second for activity
                    # and immediately execute on_idle_end files when user returns
                    if idle_time < 1:  # Less than 1 second of inactivity means user is back
                        self.update_status("System is ACTIVE", idle_time)
                        self.log_message("System is now active")
                        execute_folder_files('on_idle_end', self.log_message)
                        self.was_idle = False
                
                time.sleep(1)  # Check every second
                
            except Exception as e:
                self.log_message(f"Error in monitoring: {str(e)}")
                time.sleep(5)  # Wait longer on error
    
    def run(self):
        """Start the GUI main loop."""
        self.root.mainloop()

def get_idle_time():
    """Get the system idle time in seconds."""
    lastInputInfo = win32api.GetLastInputInfo()
    elapsed = (win32api.GetTickCount() - lastInputInfo) / 1000.0
    return elapsed

def execute_file(file_path, log_func):
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
                
        elif ext == '.ahk':
            os.startfile(str(file_path))  # uses the default .ahk association
            
        log_func(f"Executed: {file_path.name}")
    except Exception as e:
        log_func(f"Error executing {file_path.name}: {str(e)}")

def execute_folder_files(folder_path, log_func):
    """Execute all supported files in the specified folder."""
    folder = Path(folder_path)
    folder.mkdir(exist_ok=True)  # Create folder if it doesn't exist

    supported_extensions = {'.exe', '.bat', '.ps1', '.lnk', '.ahk'}
    
    executed_count = 0
    for file_path in folder.glob('*'):
        if file_path.suffix.lower() in supported_extensions:
            execute_file(file_path, log_func)
            executed_count += 1
    
    if executed_count == 0:
        log_func(f"No files to execute in {folder_path}")
    else:
        log_func(f"Executed {executed_count} file(s) from {folder_path}")

def main():
    parser = argparse.ArgumentParser(description='Monitor system idle state and execute files.')
    parser.add_argument('idle_time', type=int, nargs='?', default=600, 
                       help='Idle time threshold in seconds (default: 600)')
    args = parser.parse_args()

    # Create required folders at startup
    Path('on_idle').mkdir(exist_ok=True)
    Path('on_idle_end').mkdir(exist_ok=True)

    # Create and run the GUI
    app = IdleMonitorGUI(args.idle_time)
    app.run()

if __name__ == '__main__':
    main()
