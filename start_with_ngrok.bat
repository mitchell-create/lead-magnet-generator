@echo off
echo Starting Lead Magnet Generator with ngrok...
echo.
echo Make sure ngrok.exe is in your PATH or in this directory
echo.
cd /d "%~dp0"

echo Starting Flask server in background...
start "Flask Server" cmd /k "python layer1_slack_listener.py"

timeout /t 3 /nobreak >nul

echo Starting ngrok tunnel...
echo.
echo Your Slack Request URLs should be:
echo   Events: https://YOUR_NGROK_URL.ngrok.io/slack/events
echo   Commands: https://YOUR_NGROK_URL.ngrok.io/slack/commands
echo.
echo Press Ctrl+C to stop ngrok (server will keep running)
echo.

ngrok http 3000

pause
