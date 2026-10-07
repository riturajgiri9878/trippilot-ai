from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    app_name: str = "TripPilot AI"
    app_env: str = "development"
    debug: bool = True

    # Database
    database_url: str = "sqlite:///data/trippilot.db"

    # LLM - Gemini
    gemini_api_key: str = ""

    # LLM - NVIDIA NIM
    nvidia_api_key: str = ""
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    nvidia_model: str = "google/gemma-4-31b-it"

    # Local LLM - Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5-coder:3b"

    # Travel providers
    amadeus_client_id: str = ""
    amadeus_client_secret: str = ""

    geoapify_api_key: str = ""

    # Networking
    request_timeout: int = 10
    max_retries: int = 2

    # Security
    secret_key: str = "development-secret-change-later"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()