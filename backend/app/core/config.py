import os
from pathlib import Path
from dotenv import load_dotenv

def load_env_variables(env_path: Path) -> None:
    if env_path.exists():
        load_dotenv(dotenv_path=str(env_path), override=False)
