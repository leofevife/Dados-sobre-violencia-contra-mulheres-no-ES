# Backend API para Cloudflare D1

Este backend fornece endpoints FastAPI para receber dados e consultar o banco de dados Cloudflare D1.

## Instalação

1. Criar e ativar ambiente Python.
2. Instalar dependências:

```bash
pip install -r requirements.txt
```

## Execução

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Também é possível iniciar backend e frontend juntos a partir do workspace:

```powershell
./start.ps1
```

ou no Windows:

```cmd
start.bat
```

## Endpoints

- `GET /status` - verifica se a API está ativa.
- `POST /cloudflare/query` - executa uma query SQL no D1.
- `GET /cloudflare/health` - valida o token e a conexão com o Cloudflare D1.
- `GET /cloudflare/sample` - consulta um SQL padrão configurado.
- `POST /cloudflare/receive` - recebe dados JSON e salva em `backend/data/received_data.json`.
