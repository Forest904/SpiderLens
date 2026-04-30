from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    llm_api_key: str = Field(default="", alias="LLM_API_KEY")
    llm_base_url: str = Field(default="https://api.openai.com/v1", alias="LLM_BASE_URL")
    llm_model: str = Field(default="gpt-4o-mini", alias="LLM_MODEL")
    spider_data_dir: Path = Field(default=Path("data/spider"), alias="SPIDER_DATA_DIR")
    spiderlens_output_dir: Path = Field(default=Path("data/outputs"), alias="SPIDERLENS_OUTPUT_DIR")
    temperature: float = Field(default=0.0, alias="LLM_TEMPERATURE")


def load_settings() -> Settings:
    load_dotenv()
    return Settings()
