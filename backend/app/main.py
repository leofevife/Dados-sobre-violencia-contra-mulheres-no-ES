from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import load_env_variables

BASE_DIR = Path(__file__).resolve().parent.parent
load_env_variables(BASE_DIR / ".env")

from app.api.routes import router

import contextlib

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    from data.extrair_dados import carregar_dados_cacheados, extrair_violencia_geral
    df = carregar_dados_cacheados()
    if df is None:
        df = extrair_violencia_geral()
    app.state.df_violencia = df
    yield
    app.state.df_violencia = None

app = FastAPI(
    title="Cloudflare D1 Receiver API",
    description="API REST para receber dados e consultar o banco de dados Cloudflare D1.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
