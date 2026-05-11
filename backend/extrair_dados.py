import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def extrair_violencia_geral():
    account_id = os.getenv("ACCOUNT_ID")
    database_id = os.getenv("DATABASE_ID")
    api_token = os.getenv("API_TOKEN")

    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/d1/database/{database_id}/query"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    limit = 10000
    offset = 0
    todas_linhas = []
    
    while True:
        print(f"Extraindo linhas {offset} a {offset + limit}...")
        
        query = f"SELECT * FROM VIOLENCIA_GERAL LIMIT {limit} OFFSET {offset}"
        payload = {"sql": query}
        
        resposta = requests.post(url, headers=headers, json=payload)
        resposta.raise_for_status()
        
        dados = resposta.json()
        
        resultados = dados.get("result", [])
        if not resultados:
            break
            
        linhas = resultados[0].get("results", [])
        if not linhas:
            break
            
        todas_linhas.extend(linhas)
        
        if len(linhas) < limit:
            break
            
        offset += limit

    df = pd.DataFrame(todas_linhas)
    df = df.drop_duplicates()
    
    total_linhas = len(df)
    print(f"Total de linhas extraídas após limpeza: {total_linhas}")
    
    if total_linhas == 143375:
        print("Total de linhas coincide com o esperado (143.375).")
    else:
        print("Aviso: Total de linhas não coincide com o esperado.")
        
    return df

if __name__ == "__main__":
    df_final = extrair_violencia_geral()
