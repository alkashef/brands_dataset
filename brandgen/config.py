"""Configuration loading utilities.

Responsibility: Provide a typed configuration object and helpers to load
environment variables (optionally via a .env file) centralizing all tunables.
"""

from __future__ import annotations
from dataclasses import dataclass
import os
from dotenv import load_dotenv


@dataclass
class ChatGPTConfig:
    """Typed container for settings controlling dataset generation."""

    api_key: str
    model: str
    industries_file: str
    companies_file: str
    brands_file: str
    dataset_file: str
    max_companies_per_industry: int
    max_brands_per_company: int
    country: str
    country_specific: bool


def load_env(env_path: str = "config/.env") -> None:
    """Load environment variables from a .env file if it exists.

    Does nothing silently if the file is absent.
    """
    if os.path.exists(env_path):
        load_dotenv(env_path)


def _as_bool(value: str | None) -> bool:
    """Return True if the string represents a truthy flag.

    Accepted truthy tokens (case-insensitive): 1, true, yes, on.
    """
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def get_config() -> ChatGPTConfig:
    """Assemble configuration from environment variables with validation."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment")
    model = os.getenv("GPT_MODEL", "").strip()
    if not model:
        raise ValueError("GPT_MODEL not set in environment")

    def need(name: str) -> str:
        v = os.getenv(name, "").strip()
        if not v:
            raise ValueError(f"{name} not set in environment")
        return v

    industries_file = need("INDUSTRIES_FILE")
    companies_file = need("COMPANIES_FILE")
    brands_file = need("BRANDS_FILE")
    dataset_file = need("DATASET_FILE")
    max_companies_per_industry = int(os.getenv("MAX_COMPANIES_PER_INDUSTRY", "0") or 0)
    max_brands_per_company = int(os.getenv("MAX_BRANDS_PER_COMPANY", "0") or 0)
    country = os.getenv("COUNTRY", "").strip()
    country_specific = _as_bool(os.getenv("COUNTRY_SPECIFIC"))

    return ChatGPTConfig(
        api_key=api_key,
        model=model,
        industries_file=industries_file,
        companies_file=companies_file,
        brands_file=brands_file,
        dataset_file=dataset_file,
        max_companies_per_industry=max_companies_per_industry,
        max_brands_per_company=max_brands_per_company,
        country=country,
        country_specific=country_specific,
    )
