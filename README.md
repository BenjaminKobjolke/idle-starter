# Idle State File Executor

A GUI application that monitors the system's idle state and executes files based on idle/active transitions.

## Setup

### Automatic Installation

Run `install.bat` to automatically create a virtual environment and install all required packages.

### Manual Installation

1. Create and activate the Python virtual environment:

```bash
python -m venv venv
.\venv\Scripts\activate
```

2. Install required packages:

```bash
pip install pywin32
```

## Usage

**Important:** It's recommended to run the script with administrative privileges to ensure proper execution of all file types.

### Quick Start

Use the included batch file for easy startup:
```bash
idle_monitor.bat  # Runs with 180 seconds (3 minutes) threshold
```

### Manual Run

Run the script with the desired idle time threshold in seconds (default is 600 seconds if not specified):

```bash
python idle_monitor.py 300  # Sets idle threshold to 5 minutes
python idle_monitor.py     # Uses default threshold of 600 seconds (10 minutes)
```

### Setup Your Automation

1. Place files you want to execute when the system becomes idle in the `on_idle` folder
2. Place files you want to execute when the system becomes active in the `on_idle_end` folder

Supported file types:

-   Executable files (.exe)
-   Batch files (.bat)
-   PowerShell scripts (.ps1)
-   Windows shortcuts (.lnk)
-   AutoHotkey scripts (.ahk)

## GUI Features

The application provides a graphical interface with:

-   **Real-time status display** - Shows current system state (Active/Idle) and idle time counter
-   **Activity log** - Displays timestamped events and executed files
-   **Test buttons** (NEW):
    - **"Test idle"** - Manually trigger execution of files in the `on_idle` folder for testing
    - **"Test idle end"** - Manually trigger execution of files in the `on_idle_end` folder for testing
    - Useful for testing your automation without waiting for actual idle time
-   **Clear log** - Button to clear the activity log
-   **Dark theme** - Easy on the eyes during extended monitoring

## How It Works

The application will:

-   Monitor system idle state continuously
-   Execute all supported files in `on_idle` folder when system becomes idle
-   Execute all supported files in `on_idle_end` folder when system becomes active again
-   Display all activities in the GUI log window
-   Continue monitoring until the Exit button is clicked or window is closed

## Additional Files

-   `install.bat` - Automatically sets up the Python virtual environment and installs dependencies
-   `idle_monitor.bat` - Quick launcher that runs the monitor with 3-minute idle threshold
-   `compile_exe.bat` - Creates a standalone .exe file (requires PyInstaller)

## Notes

-   The script requires administrative privileges to execute some file types
-   Both `on_idle` and `on_idle_end` folders are excluded from git
-   The folders will be created automatically when the application starts if they don't exist
