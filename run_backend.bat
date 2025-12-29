@echo off
cd /d "%~dp0"
echo Starting Backend Server...
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
pause
