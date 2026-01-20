from dataclasses import dataclass
from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from optiak.labs.utils import singleton

T = TypeVar("T")


@dataclass
class Paged(Generic[T]):
    total: int
    data: List[T]

    @staticmethod
    def empty():
        return Paged(total=0, data=[])


@dataclass
class Pagination:
    max: int = 10
    offset: int = 0


class ObservabilityConfig(BaseModel):
    metrics_url: str = Field(default="http://localhost:15200/v1/metrics")
    traces_url: str = Field(default="http://localhost:15200/v1/traces")
    service_name: str = Field(default="optiak.api")


class DatabaseConfig(BaseModel):
    type: str = Field(default="postgresql")
    name: str = Field(default="optiak")
    username: str = Field(default="username")
    password: str = Field(default="password")
    driver: str = Field(default="pg8000")
    host: str = Field(default="postgres-grafana-svc")
    port: int = Field(default=5432)

    def get_url(self):
        return "{}+{}://{}:{}@{}:{}/{}".format(
            self.type,
            self.driver,
            self.username,
            self.password,
            self.host,
            self.port,
            self.name,
        )


class CryptoConfig(BaseModel):
    # to get a string like this run:
    # openssl rand -hex 32
    secret_key: str = Field(
        default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    algorithm: str = Field(default="HS256")
    salt: str = Field(default="$2b$10$Yxoh.mrE75jD1U.U7dBYV.")
    token_expires_minutes: int = Field(default=30)


class MailConfig(BaseModel):
    host: str = Field(default="mailpit-svc")
    port: int = Field(default=1025)
    default_sender: str = Field(default="system@optiak.com")


@singleton
class OptiakConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="OPTIAK_API")

    crypto: CryptoConfig = CryptoConfig()
    db: DatabaseConfig = DatabaseConfig()
    observability: ObservabilityConfig = ObservabilityConfig()
    mail: MailConfig = MailConfig()


class ConfigurationSingleton:
    @staticmethod
    def instance():
        return OptiakConfiguration()
