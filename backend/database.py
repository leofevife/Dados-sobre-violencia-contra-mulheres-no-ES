import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import params
import requests
from dotenv import load_dotenv

CLOUDFLARE_API_BASE = "https://api.cloudflare.com/client/v4"
TABLE_NAME_RE = re.compile(r"^[A-Za-z0-9_]+$")


def load_env_variables(env_path: Path) -> None:
    if env_path.exists():
        load_dotenv(dotenv_path=str(env_path), override=False)


class CloudflareD1Client:
    def __init__(self):
        self.account_id = os.getenv("ACCOUNT_ID")
        self.database_id = os.getenv("DATABASE_ID")
        self.api_token = os.getenv("API_TOKEN")

        if not self.account_id or not self.database_id or not self.api_token:
            raise ValueError(
                "ACCOUNT_ID, DATABASE_NAME/DATABASE_ID e API_TOKEN devem estar definidos no arquivo .env"
            )

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def query(self, statement: str, params: Optional[Dict[str, Any]] = None) -> Any:        
        payload = {"sql": statement}
        if params:
            payload["params"] = params

        urls = [
            f"{CLOUDFLARE_API_BASE}/accounts/{self.account_id}/d1/database/{self.database_id}/query",
            f"{CLOUDFLARE_API_BASE}/accounts/{self.account_id}/d1/databases/{self.database_id}/query",
        ]

        response = None
        for url in urls:
            response = requests.post(url, headers=self._headers(), json=payload, timeout=30)
            if response.status_code != 404:
                break

        if response is None:
            raise RuntimeError("Não foi possível conectar ao endpoint Cloudflare D1.")

        if response.status_code == 401:
            raise RuntimeError(
                "401 Unauthorized: verifique se o API_TOKEN Cloudflare tem permissão para acessar D1 "
                "e se ACCOUNT_ID/DATABASE_ID estão corretos."
            )

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            payload_text = response.text
            raise RuntimeError(
                f"Cloudflare D1 HTTP error {response.status_code}: {payload_text}"
            ) from http_err

        data = response.json()
        if not data.get("success"):
            raise RuntimeError(f"Cloudflare D1 returned failure: {data}")

        return data.get("result")

    def list_tables(self) -> List[str]:
        rows = self.query(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
        table_names: List[str] = []
        for row in rows:
            if isinstance(row, dict) and "name" in row:
                table_names.append(str(row["name"]))
            elif isinstance(row, (list, tuple)) and row:
                table_names.append(str(row[0]))
        return table_names

    def select_table(self, table_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        if not TABLE_NAME_RE.match(table_name):
            raise ValueError("Nome da tabela inválido")
        statement = f"SELECT * FROM {table_name} LIMIT {limit}"
        rows = self.query(statement)
        return rows if isinstance(rows, list) else []
