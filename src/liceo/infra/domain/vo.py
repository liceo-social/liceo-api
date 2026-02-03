from dataclasses import dataclass
from datetime import datetime
from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from liceo.labs.utils import singleton

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
    service_name: str = Field(default="liceo.api")


class DatabaseConfig(BaseModel):
    type: str = Field(default="postgresql")
    name: str = Field(default="liceo")
    username: str = Field(default="username")
    password: str = Field(default="password")
    driver: str = Field(default="pg8000")
    host: str = Field(default="postgres-svc")
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
    default_sender: str = Field(default="system@liceo.com")


@singleton
class LiceoConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LICEO_API")

    crypto: CryptoConfig = CryptoConfig()
    db: DatabaseConfig = DatabaseConfig()
    observability: ObservabilityConfig = ObservabilityConfig()
    mail: MailConfig = MailConfig()


class ConfigurationSingleton:
    @staticmethod
    def instance():
        return LiceoConfiguration()


class AuditInfo(Generic[T]):
    created_by: T
    created_at: datetime
    last_modified_by: T
    last_modified_at: datetime
    deleted_by: T | None
    deleted_at: datetime | None

    def __init__(self, created_by: T):
        creation_time = datetime.now()
        self.created_by = created_by
        self.created_at = creation_time
        self.last_modified_by = created_by
        self.last_modified_at = creation_time

    def modified(self, user_id: T):
        self.last_modified_by = user_id
        self.last_modified_at = datetime.now()

    def deleted(self, user_id: T):
        deletion_time = datetime.now()
        self.last_modified_by = user_id
        self.last_modified_at = deletion_time
        self.deleted_by = user_id
        self.deleted_at = deletion_time
