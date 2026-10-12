@echo off
echo Starting Adaptive Lightweight NIDS Backend Server on http://localhost:8000...
cd /d "%~dp0"
python run_server.py
pause
