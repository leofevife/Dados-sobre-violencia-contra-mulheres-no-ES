@echo off
set ROOT=%~dp0
start "Backend" powershell -NoExit -Command "Set-Location -LiteralPath '%ROOT%backend'; py -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
start "Frontend" powershell -NoExit -Command "Set-Location -LiteralPath '%ROOT%frontend'; npm run dev"
echo Backend disponível em http://localhost:8000
echo Frontend disponível em http://localhost:5173
