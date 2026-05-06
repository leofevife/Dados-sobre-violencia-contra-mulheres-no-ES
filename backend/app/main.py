from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import load_env_variables

BASE_DIR = Path(__file__).resolve().parent.parent
load_env_variables(BASE_DIR / ".env")

from app.api.routes import router

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

app.include_router(router)
