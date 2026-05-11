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

## Processamento de Dados (Cache e Inicialização)

O backend agora conta com um script de extração automática (`backend/data/extrair_dados.py`) que é executado durante o processo de inicialização da aplicação FastAPI (via `lifespan`).
- Na primeira execução (ou quando o arquivo `.csv` não existir), o sistema fará requisições paginadas à API do Cloudflare D1, extrairá todos os registros da tabela configurada e os salvará no arquivo `backend/data/violencia_geral.csv`.
- Nas inicializações subsequentes, o backend lerá rapidamente esse arquivo CSV local para a memória usando **Pandas**, tornando o startup praticamente instantâneo e economizando requisições da API. O DataFrame fica disponível no estado global do servidor (`app.state.df_violencia`) para futuras análises de dados.
