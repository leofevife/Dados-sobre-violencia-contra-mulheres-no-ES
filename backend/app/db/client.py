import os
from typing import Any, Dict, List
import requests


class SupabaseClient:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")

        if not self.url or not self.key:
            raise ValueError(
                "SUPABASE_URL e SUPABASE_KEY devem estar definidos no arquivo .env"
            )

    def _headers(self) -> Dict[str, str]:
        return {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
        }

    def get_view(self, view_name: str, limit: int = 1000, offset: int = 0) -> List[Dict[str, Any]]:
        url = f"{self.url}/rest/v1/{view_name}?select=*&limit={limit}&offset={offset}"
        headers = self._headers()
        headers["Prefer"] = "count=exact"

        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 401:
            raise RuntimeError("401 Unauthorized: verifique a SUPABASE_KEY.")

        response.raise_for_status()
        return response.json()

    def get_view_all(self, view_name: str) -> List[Dict[str, Any]]:
        all_rows: List[Dict[str, Any]] = []
        limit = 1000
        offset = 0

        while True:
            rows = self.get_view(view_name, limit=limit, offset=offset)
            all_rows.extend(rows)
            if len(rows) < limit:
                break
            offset += limit

        return all_rows
