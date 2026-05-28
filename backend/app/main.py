from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import load_env_variables

BASE_DIR = Path(__file__).resolve().parent.parent
load_env_variables(BASE_DIR / ".env")

from app.api.routes import router

app = FastAPI(
    title="Supabase API",
    description="API REST para consultar dados no Supabase.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
