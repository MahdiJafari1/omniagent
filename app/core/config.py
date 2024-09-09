from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    TTILE: str = "OmniAgent API"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Multi-Agent System to solve complex problems using RAG"
    TAGS_METADATA: list[dict] = [
        # {"name": "tasks", "description": "Operations related to tasks"},
        # {"name": "agents", "description": "Operations related to agents"},
    ]
    TOS: str = "https://www.example.com/tos"
    CONTACT: dict = {
        "name": "Mahdi Jafari",
        "url": "https://www.linkedin.com/in/mahdijafari12/",
        "email": "jafarimahdi.me@gmail.com",
    }
    LICENSE: dict = {"name": "MIT", "url": "https://www.example.com/license"}
    ROOT_DIR: Path = Path(__file__).resolve().parent.parent


settings = Settings()
