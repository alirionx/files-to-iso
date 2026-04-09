import os
from pydantic import BaseModel

class Settings(BaseModel):
    tinydb_path: str = os.environ.get("TINYDB_PATH", "./files-to-iso.db")
    app_port: int = int(os.environ.get("APP_PORT", "5000"))
    app_debug: bool = bool(os.environ.get("APP_DEBUG", "True"))
    static_html_folder: str = "static"

settings = Settings()