"""JSON Schemas for structured model responses.

Responsibility: Define response formats for companies and brands so the
OpenAI API returns deterministic JSON matching expected dataset shape.
"""

from __future__ import annotations
from typing import Any, Dict


def companies_schema() -> Dict[str, Any]:
    """Return JSON schema dict for companies response."""
    return {
        "name": "companies_schema",
        "schema": {
            "type": "object",
            "properties": {
                "companies": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "company_name": {"type": "string"},
                            "headquarters_country": {"type": "string"},
                            "main_industry_activities": {"type": "string"},
                        },
                        "required": [
                            "company_name",
                            "headquarters_country",
                            "main_industry_activities",
                        ],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["companies"],
            "additionalProperties": False,
        },
    }


def brands_schema() -> Dict[str, Any]:
    """Return JSON schema dict for brands response."""
    return {
        "name": "brands_schema",
        "schema": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {"type": "string"},
                            "invoice_example": {"type": "string"},
                            "gpc_segment": {"type": "string"},
                            "gpc_family": {"type": "string"},
                            "gpc_class": {"type": "string"},
                            "gpc_brick": {"type": "string"},
                        },
                        "required": [
                            "name",
                            "type",
                            "invoice_example",
                            "gpc_segment",
                            "gpc_family",
                            "gpc_class",
                            "gpc_brick",
                        ],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["items"],
            "additionalProperties": False,
        },
    }
