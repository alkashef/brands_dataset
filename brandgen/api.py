"""API interaction layer.

Responsibility: Own OpenAI client creation and schema-constrained calls for
companies and brands generations.
"""

from __future__ import annotations
import json
from typing import List, Dict
from openai import OpenAI
from .schemas import companies_schema, brands_schema


def create_client(api_key: str) -> OpenAI:
    """Instantiate an OpenAI client with the provided API key."""
    return OpenAI(api_key=api_key)


def ask_companies(client: OpenAI, model: str, prompt: str) -> List[Dict[str, str]]:
    """Request a structured list of companies for a single industry section.

    Returns list of company dicts matching companies_schema().
    """
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_schema", "json_schema": companies_schema()},
        temperature=0.2,
    )
    content = completion.choices[0].message.content
    return json.loads(content).get("companies", [])


def ask_brands(client: OpenAI, model: str, prompt: str) -> List[Dict[str, str]]:
    """Request structured brand / product / service items for one company.

    Returns list of brand dicts matching brands_schema().
    """
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_schema", "json_schema": brands_schema()},
        temperature=0.2,
    )
    content = completion.choices[0].message.content
    return json.loads(content).get("items", [])
