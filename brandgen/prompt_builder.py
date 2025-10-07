"""Prompt assembly utilities.

Responsibility: Turn template constants into concrete prompts using runtime
parameters (section labels, company names, optional country filtering).
"""

from __future__ import annotations
from .prompt import (
    BASE_PROMPT_TEMPLATE,
    companies_prompt_template,
    brands_prompt_template,
    companies_country_prompt_template,
    brands_country_prompt_template,
    companies_groups_prompt_template,
    companies_groups_country_prompt_template,
)


def build_prompt(question: str) -> str:
    """Wrap a specific question with the shared base system instructions."""
    return f"{BASE_PROMPT_TEMPLATE}\n\n{question.strip()}"


def build_companies_prompt(section_label: str, country: str, use_country: bool) -> str:
    """Return companies prompt, optionally country-specific."""
    # Use simple replacement instead of str.format to avoid interpreting JSON braces.
    if use_country and country:
        return (
            companies_country_prompt_template
            .replace('{section}', section_label)
            .replace('{country}', country)
        )
    return companies_prompt_template.replace('{section}', section_label)


def build_companies_groups_prompt(group_data: dict[str, str], country: str, use_country: bool) -> str:
    """Return companies prompt for ISIC groups (level 3), optionally country-specific."""
    template = companies_groups_country_prompt_template if use_country and country else companies_groups_prompt_template
    
    prompt = (template
        .replace('{section_name}', group_data.get('section_name', ''))
        .replace('{division_name}', group_data.get('division_name', ''))
        .replace('{group_name}', group_data.get('group_name', ''))
        .replace('{includes}', group_data.get('includes', ''))
        .replace('{excludes}', group_data.get('excludes', ''))
    )
    
    if use_country and country:
        prompt = prompt.replace('{country}', country)
    
    return prompt


def build_brands_prompt(company: str, country: str, use_country: bool) -> str:
    """Return brands prompt, optionally country-specific."""
    if use_country and country:
        return (
            brands_country_prompt_template
            .replace('{company}', company)
            .replace('{country}', country)
        )
    return brands_prompt_template.replace('{company}', company)
