"""Flatten nested data structures to CSV."""

from __future__ import annotations
from pathlib import Path
import csv
from typing import Dict, List


def flatten_to_csv(
    sections_companies: Dict[str, List[dict]],
    brands: Dict[str, List[dict]],
    csv_path: str,
) -> None:
    """Emit a tabular CSV joining companies with their brands.

    If a company has no brands an empty brand row is written.
    """
    fieldnames = [
        "industry_section",
        "company_name",
        "headquarters_country",
        "main_industry_activities",
        "brand_name",
        "brand_type",
        "invoice_example",
        "gpc_segment",
        "gpc_family",
        "gpc_class",
        "gpc_brick",
    ]
    Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
    with Path(csv_path).open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for section, companies in sections_companies.items():
            for company in companies:
                if not isinstance(company, dict):
                    continue
                c_name = company.get("company_name", "")
                c_country = company.get("headquarters_country", "")
                c_activities = company.get("main_industry_activities", "")
                company_brands = brands.get(c_name, [])
                if not company_brands:
                    writer.writerow(
                        {
                            "industry_section": section,
                            "company_name": c_name,
                            "headquarters_country": c_country,
                            "main_industry_activities": c_activities,
                            "brand_name": "",
                            "brand_type": "",
                            "invoice_example": "",
                            "gpc_segment": "",
                            "gpc_family": "",
                            "gpc_class": "",
                            "gpc_brick": "",
                        }
                    )
                    continue
                for b in company_brands:
                    if not isinstance(b, dict):
                        continue
                    writer.writerow(
                        {
                            "industry_section": section,
                            "company_name": c_name,
                            "headquarters_country": c_country,
                            "main_industry_activities": c_activities,
                            "brand_name": b.get("name", ""),
                            "brand_type": b.get("type", ""),
                            "invoice_example": b.get("invoice_example", ""),
                            "gpc_segment": b.get("gpc_segment", ""),
                            "gpc_family": b.get("gpc_family", ""),
                            "gpc_class": b.get("gpc_class", ""),
                            "gpc_brick": b.get("gpc_brick", ""),
                        }
                    )
