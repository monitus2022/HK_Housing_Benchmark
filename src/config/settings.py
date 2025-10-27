from pathlib import Path
from typing import Dict, Optional
import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from logger import housing_logger
from dotenv import load_dotenv

working_dir = Path(__file__).parent.parent.parent
config_path = working_dir / "src" / "config" / "config.yml"
env_path = working_dir / ".env"


def load_environment():
    """Load environment variables from .env file if it exists."""
    if env_path.exists():
        housing_logger.debug(f"Loading environment variables from {env_path}")
        load_dotenv(dotenv_path=env_path)


def load_yaml_config():
    """Load YAML configuration file."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# Load environment and config
load_environment()
yaml_data = load_yaml_config()


# Cloud Storage Configurations


class CloudStorageConfig(BaseModel):
    service_type: str = "cloudflare"


class CloudflareConfig(BaseModel):
    endpoint_url: str
    bucket_name: str
    region: str = "auto"
    datahub_folder_name: str = "data"


class AWSConfig(BaseModel):
    bucket_name: str
    region: str = "us-east-1"


class CloudStorageSecrets(BaseSettings):
    account_id: Optional[str] = Field(
        None, alias="cloudflare_account_id"
    )  # Only needed for Cloudflare
    access_key_id: str = Field(alias="cloud_storage_access_key_id")
    secret_access_key: str = Field(alias="cloud_storage_secret_access_key")

    model_config = SettingsConfigDict(
        env_file=env_path if env_path.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Local Storage Configurations


class BaseStorageConfig(BaseModel):
    path: str
    files: Dict[str, str]


class RAGStorageConfig(BaseModel):
    path: str
    files: Dict[str, str]
    settings: Optional[Dict[str, int]] = None


class StorageConfig(BaseModel):
    root_path: str
    agency: BaseStorageConfig
    wiki: BaseStorageConfig
    rag: RAGStorageConfig


# LLM Configurations


class LLMOllamaConfig(BaseModel):
    default_model: str = "llama3.1:latest"


class LLMConfig(BaseModel):
    ollama: LLMOllamaConfig


class Settings(BaseSettings):
    storage: StorageConfig
    cloud_storage: CloudStorageConfig
    cloudflare: CloudflareConfig
    aws: AWSConfig
    llm: LLMConfig

    model_config = SettingsConfigDict(
        extra="allow",
        env_file=env_path if env_path.exists() else None,
        env_file_encoding="utf-8",
    )
    housing_logger.info("Housing Benchmark Configuration Loaded Successfully")


# Create separate settings instances
housing_benchmark_config = Settings(**yaml_data)
cloud_storage_secrets = CloudStorageSecrets()
