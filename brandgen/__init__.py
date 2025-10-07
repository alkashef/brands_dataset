"""brandgen package exposing public API.

This package organizes dataset generation into clear layers:
- config: environment & configuration loading.
- schemas: JSON schema definitions for structured responses.
- prompt: static prompt templates.
- prompt_builder: runtime assembly of prompts.
- api: OpenAI client + schema constrained calls.
- persist: JSON file loading/saving helpers.
- flatten: CSV export utilities.

The top-level exports below present a minimal surface area for users.
"""

from .config import load_env, get_config, ChatGPTConfig
from .api import create_client, ask_companies, ask_brands
from .prompt_builder import (
    build_prompt,
    build_companies_prompt,
    build_brands_prompt,
    build_companies_groups_prompt,
)
from .persist import load_sections, load_json, save_json, load_companies, load_isic_groups
from .flatten import flatten_to_csv
from .logger import configure_logger

__all__ = [
    "load_env",
    "get_config",
    "ChatGPTConfig",
    "create_client",
    "ask_companies",
    "ask_brands",
    "build_prompt",
    "build_companies_prompt",
    "build_brands_prompt",
    "build_companies_groups_prompt",
    "load_sections",
    "load_json",
    "save_json",
    "flatten_to_csv",
    "configure_logger",
    "load_companies",
    "load_isic_groups",
]
