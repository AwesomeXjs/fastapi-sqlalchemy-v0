from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(
    __file__
).parent.parent  # относительный путь к нужной дериктории где должна лежать бд


class Settings(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    db_echo: bool = True


settings = Settings()
