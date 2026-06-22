"""Central application configuration.

All settings are read from environment variables (or the local .env file),
validated, and exposed as a single `settings` object the whole app imports.
"""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Application ---
    app_name: str = "SupportGenie"
    environment: str = "local"

    # --- Groq (LLM) ---
    groq_api_key: SecretStr | None = None

    # --- JWT auth ---
    jwt_secret_key: SecretStr | None = None
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60


settings = Settings()