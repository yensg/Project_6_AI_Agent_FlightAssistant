from pathlib import Path
from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import Optional

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_api_version: str = "2023-03-15-preview"
    cosmos_connection_string: Optional[str] = None
    flight_api_key: Optional[str] = None
    flight_api_base_url: Optional[str] = None

    @field_validator('azure_openai_api_key', 'azure_openai_endpoint')
    @classmethod
    def validate_required_fields(cls, v, field):
        if not v:
            raise ValueError(f"{field.name} is required")
        return v

    class Config:
        env_file = BASE_DIR / ".env"

_settings = None

def get_settings() -> Settings: # to ensure only one same instance is created
    global  _settings
    if _settings is None:
        _settings = Settings()
    return _settings
