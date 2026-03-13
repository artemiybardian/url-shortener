from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379

    shortener_grpc_host: str = "shortener-service"
    shortener_grpc_port: int = 50051

    analytics_grpc_host: str = "analytics-service"
    analytics_grpc_port: int = 50052

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"

    @property
    def shortener_grpc_address(self) -> str:
        return f"{self.shortener_grpc_host}:{self.shortener_grpc_port}"

    @property
    def analytics_grpc_address(self) -> str:
        return f"{self.analytics_grpc_host}:{self.analytics_grpc_port}"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
