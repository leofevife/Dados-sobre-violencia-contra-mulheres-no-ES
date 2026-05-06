$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backend = Join-Path $root 'backend'
$frontend = Join-Path $root 'frontend'

Write-Host 'Iniciando backend...'
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location -LiteralPath '$backend'; py -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

Write-Host 'Iniciando frontend...'
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location -LiteralPath '$frontend'; npm run dev"

Write-Host 'Backend disponível em http://localhost:8000'
Write-Host 'Frontend disponível em http://localhost:5173'
