@echo off
call activate_environment.bat
call pyinstaller --name IdleStarter --onefile --windowed idle_monitor.py 
xcopy on_idle dist\on_idle /E /Y /I
xcopy on_idle_end dist\on_idle_end /E /Y /I
pause
