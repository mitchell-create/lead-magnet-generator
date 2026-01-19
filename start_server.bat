@echo off
echo Starting Lead Magnet Generator Server...
echo.
echo Server will run on http://localhost:3000
echo Keep this window open while using the app.
echo.
cd /d "%~dp0"
python layer1_slack_listener.py
pause
