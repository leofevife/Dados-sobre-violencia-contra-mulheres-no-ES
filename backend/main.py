import json
import os
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from database import CloudflareD1Client, load_env_variables

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

load_env_variables(BASE_DIR / ".env")

app = FastAPI(
    title="Cloudflare D1 Receiver API",
    description="API REST para receber dados e consultar o banco de dados Cloudflare D1.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cf_client = CloudflareD1Client()


class SqlQuery(BaseModel):
    statement: str = Field(..., description="SQL statement to execute on Cloudflare D1")


class ReceivedData(BaseModel):
    data: dict = Field(..., description="Payload data sent from the source")


@app.get("/status")
def status():
    return {
        "status": "ok",
        "cloudflare_account_id": cf_client.account_id,
        "cloudflare_database_id": cf_client.database_id,
    }


@app.get("/cloudflare/health")
def cloudflare_health():
    try:
        result = cf_client.query("SELECT 1")
        return {
            "success": True,
            "message": "Conexão com Cloudflare D1 verificada com sucesso.",
            "query_result": result,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail={
                "error": str(exc),
                "hint": "Verifique se o API_TOKEN tem permissão para acessar Cloudflare D1 e se ACCOUNT_ID/DATABASE_ID estão corretos.",
            },
        )


@app.post("/cloudflare/query")
def query_cloudflare(query: SqlQuery):
    try:
        result = cf_client.query(query.statement)
        return {"success": True, "result": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/cloudflare/tables")
def list_tables():
    try:
        tables = cf_client.list_tables()
        return {"success": True, "tables": tables}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/cloudflare/table/{table_name}")
def get_table(table_name: str):
    try:
        rows = cf_client.select_table(table_name)
        return {"success": True, "rows": rows}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/cloudflare/receive")
def receive_data(payload: ReceivedData):
    file_path = DATA_DIR / "received_data.json"
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload.data, f, ensure_ascii=False, indent=2)
        return {"success": True, "message": "Dados recebidos e salvos com sucesso.", "path": str(file_path)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/cloudflare/sample")
def sample_query():
    sql = os.getenv("DEFAULT_CLOUDFLARE_SQL", "SELECT * FROM my_table LIMIT 100")
    try:
        result = cf_client.query(sql)
        return {"success": True, "sql": sql, "result": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
