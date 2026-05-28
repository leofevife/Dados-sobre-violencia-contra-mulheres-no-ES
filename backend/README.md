# Backend API para Supabase

Este backend fornece endpoints FastAPI para consultar dados no banco Supabase.

## Instalação

1. Criar e ativar ambiente Python.
2. Instalar dependências:

```bash
pip install -r requirements.txt
```

## Execução

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
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
- `GET /supabase/health` - valida a conexão com o Supabase.
- `GET /supabase/view/incidencias_hora` - retorna os dados da view `view_incidencias_hora`.
