"""Prompt template definitions for the brands dataset CLI."""

from __future__ import annotations


BASE_PROMPT_TEMPLATE = (
  "You are a disciplined data extraction engine. "
  "Return ONLY valid JSON matching the provided schema instructions—no code fences, no prose, no markdown, no explanations. "
  "If uncertain about a field, use an empty string. Never hallucinate extra keys."
)


companies_prompt_template = (
  "You are an industry research assistant. Using ISIC Rev.4 Section {section} as the scope, "
  "identify the top 10 global companies operating in this section based on market share. "
  "For each company, provide the following fields in JSON format:\n\n"
  "{\n"
  '  "company_name": "",\n'
  '  "headquarters_country": "",\n'
  '  "main_industry_activities": ""\n'
  "}\n"
  "Return only valid JSON (no explanations, text, or formatting outside the JSON array)."
)


brands_prompt_template = (
  "You are a business classification assistant. "
  "Focus strictly on the company named: {company}. "
  "List the top 10 distinct brands / products / services likely to appear as individual invoice line items. "
  "Return ONLY a single JSON object with this exact shape (no code fences, no extra commentary):\n"
  "{\n"
  "  \"items\": [\n"
  "    {\n"
  "      \"name\": \"\",\n"
  "      \"type\": \"\",\n"
  "      \"invoice_example\": \"\",\n"
  "      \"gpc_segment\": \"\",\n"
  "      \"gpc_family\": \"\",\n"
  "      \"gpc_class\": \"\",\n"
  "      \"gpc_brick\": \"\"\n"
  "    }\n"
  "  ]\n"
  "}\n"
  "Rules: (1) No markdown. (2) Do not include more than 10 items. (3) Each field must be a concise string."
)

companies_country_prompt_template = (
  "You are an industry research assistant. Using ISIC Rev.4 Section {section} as the scope, "
  "identify the top 10 companies headquartered in {country} operating in this section (or strongly associated with {country}). "
  "For each company, provide the following fields in JSON format:\n\n"
  "{\n"
  '  \"company_name\": \"\",\n'
  '  \"headquarters_country\": \"\",\n'
  '  \"main_industry_activities\": \"\"\n'
  "}\n"
  "Return only valid JSON (no explanations, text, or formatting outside the JSON array)."
)

brands_country_prompt_template = (
  "You are a business classification assistant. "
  "Focus strictly on the company named: {company}. Only consider brands / products / services originating from or primarily marketed in {country}. "
  "List the top 10 distinct brands / products / services likely to appear as individual invoice line items. "
  "Return ONLY a single JSON object with this exact shape (no code fences, no extra commentary):\n"
  "{\n"
  "  \"items\": [\n"
  "    {\n"
  "      \"name\": \"\",\n"
  "      \"type\": \"\",\n"
  "      \"invoice_example\": \"\",\n"
  "      \"gpc_segment\": \"\",\n"
  "      \"gpc_family\": \"\",\n"
  "      \"gpc_class\": \"\",\n"
  "      \"gpc_brick\": \"\"\n"
  "    }\n"
  "  ]\n"
  "}\n"
  "Rules: (1) No markdown. (2) Do not include more than 10 items. (3) Each field must be a concise string."
)

companies_groups_prompt_template = (
  "You are an industry research assistant. Using ISIC Rev.5 classification, "
  "focus on this specific industry group:\n"
  "- Section: {section_name}\n" 
  "- Division: {division_name}\n"
  "- Group: {group_name}\n"
  "- Includes: {includes}\n"
  "- Excludes: {excludes}\n\n"
  "Identify the top 10 global companies operating specifically in this group based on market share. "
  "For each company, provide the following fields in JSON format:\n\n"
  "{\n"
  '  "company_name": "",\n'
  '  "headquarters_country": "",\n'
  '  "main_industry_activities": ""\n'
  "}\n"
  "Return only valid JSON (no explanations, text, or formatting outside the JSON array)."
)

companies_groups_country_prompt_template = (
  "You are an industry research assistant. Using ISIC Rev.5 classification, "
  "focus on this specific industry group:\n"
  "- Section: {section_name}\n"
  "- Division: {division_name}\n" 
  "- Group: {group_name}\n"
  "- Includes: {includes}\n"
  "- Excludes: {excludes}\n\n"
  "Identify the top 10 companies headquartered in {country} operating specifically in this group (or strongly associated with {country}). "
  "For each company, provide the following fields in JSON format:\n\n"
  "{\n"
  '  "company_name": "",\n'
  '  "headquarters_country": "",\n'
  '  "main_industry_activities": ""\n'
  "}\n"
  "Return only valid JSON (no explanations, text, or formatting outside the JSON array)."
)

__all__ = [
  "BASE_PROMPT_TEMPLATE",
  "companies_prompt_template",
  "brands_prompt_template",
  "companies_country_prompt_template",
  "brands_country_prompt_template",
  "companies_groups_prompt_template",
  "companies_groups_country_prompt_template",
  ]
