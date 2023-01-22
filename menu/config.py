from pydantic import BaseSettings


class DBSettings(BaseSettings):
    username: str
    password: str
    database: str
    host: str
    port: str
    service: str

    class Config:
        env_prefix = "DB_"
        env_file = ".env"