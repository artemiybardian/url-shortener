from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    shortener_db_name: str = "shortener_db"

    shortener_grpc_port: int = 50051

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.shortener_db_name}"
        )

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
