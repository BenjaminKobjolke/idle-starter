# Idle State File Executor

This script monitors the system's idle state and executes files based on idle/active transitions.

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

1. Place files you want to execute when the system becomes idle in the `on_idle` folder
2. Place files you want to execute when the system becomes active in the `on_idle_end` folder

Supported file types:

-   Executable files (.exe)
-   Batch files (.bat)
-   PowerShell scripts (.ps1)
-   Windows shortcuts (.lnk)
-   AutoHotkey scripts (.ahk)

Run the script with the desired idle time threshold in seconds (default is 600 seconds if not specified):

```bash
python idle_monitor.py 300  # Sets idle threshold to 5 minutes
python idle_monitor.py     # Uses default threshold of 600 seconds (10 minutes)
```

The script will:

-   Monitor system idle state
-   Execute all supported files in `on_idle` folder when system becomes idle
-   Execute all supported files in `on_idle_end` folder when system becomes active again
-   Continue monitoring until interrupted with Ctrl+C

## Notes

-   The script requires administrative privileges to execute some file types
-   Both `on_idle` and `on_idle_end` folders are excluded from git
