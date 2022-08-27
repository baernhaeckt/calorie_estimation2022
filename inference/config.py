import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str = os.environ.get("ENV", default="development")


# Init the settings of the application on startup
settings: Settings = Settings()
