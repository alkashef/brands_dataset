"""Dataset generation orchestrator.

Uses the internal brandgen package modules for:
- configuration loading
- prompt construction
- OpenAI schema-constrained calls
- persistence (JSON save/load)
- CSV flattening
"""

from __future__ import annotations
from pathlib import Path
import json
from brandgen import (
	load_env,
	get_config,
	create_client,
	ask_companies,
	ask_brands,
	load_sections,
	flatten_to_csv,
	build_prompt,
	build_companies_prompt,
	build_brands_prompt,
	load_companies,
	configure_logger,
)
import logging
from tqdm import tqdm
import time


def _collect_section_responses(
	client,
	model: str,
	sections: dict[int, str],
	limit: int,
	country: str,
	use_country: bool,
	logger,
	dry_run: bool,
) -> dict[str, list[dict[str, str]]]:
	"""Fetch companies per section.

	Logs progress and truncation events when limits are applied.
	"""
	responses: dict[str, list[dict[str, str]]] = {}
	total = len(sections)
	logger.info(f"Starting company generation for {total} sections (limit={limit or 'none'})")
	for idx, section_index in enumerate(tqdm(sorted(sections), desc="Sections", unit="section"), start=1):
		label = sections[section_index]
		if dry_run:
			# Create 3 mock companies per section (or limit if smaller)
			mock_count = 3 if limit == 0 else min(3, limit)
			companies = [
				{
					"company_name": f"company{n}_section{idx}",
					"headquarters_country": country or "Unknown",
					"main_industry_activities": f"Activities for section {label}",
				}
				for n in range(1, mock_count + 1)
			]
		else:
			question = build_companies_prompt(label, country, use_country).strip()
			prompt_str = build_prompt(question)
			companies = ask_companies(client, model, prompt_str)
		original_count = len(companies)
		if limit > 0 and original_count > limit:
			companies = companies[:limit]
			logger.debug(f"Truncated companies {original_count}->{len(companies)} for section {label}")
		responses[label] = companies
	logger.info("Company generation complete")
	return responses

def _collect_brand_responses(
	client,
	model: str,
	companies: list[str],
	limit: int,
	country: str,
	use_country: bool,
	logger,
	dry_run: bool,
) -> dict[str, list[dict[str, str]]]:
	"""Fetch brand/product/service items for each company with logging."""
	results: dict[str, list[dict[str, str]]] = {}
	total = len(companies)
	logger.info(f"Starting brand generation for {total} companies (limit={limit or 'none'})")
	for name in tqdm(companies, desc="Brands", unit="company"):
		if dry_run:
			mock_count = 2 if limit == 0 else min(2, limit)
			items = [
				{
					"name": f"brand{b}_{name}",
					"type": "mock",
					"invoice_example": f"Invoice line for brand{b}_{name}",
					"gpc_segment": "00",
					"gpc_family": "000",
					"gpc_class": "0000",
					"gpc_brick": "000000",
				}
				for b in range(1, mock_count + 1)
			]
		else:
			prompt = build_prompt(build_brands_prompt(name, country, use_country))
			items = ask_brands(client, model, prompt)
		original_count = len(items)
		if limit > 0 and original_count > limit:
			items = items[:limit]
			logger.debug(f"Truncated brands {original_count}->{len(items)} for company {name}")
		results[name] = items
	logger.info("Brand generation complete")
	return results


def ask_run_mode(companies_path: Path, brands_path: Path) -> str:
	"""Ask user which mode to run.

	Returns one of:
	- 'both'   : generate companies then brands then CSV
	- 'brands' : generate brands (needs existing companies JSON) then CSV
	- 'csv'    : only regenerate CSV from existing companies + brands JSON
	"""
	print("Select run mode:")
	print("  1) Generate companies then brands (full run)")
	print("  2) Skip companies (brands only, requires companies file)")
	print("  3) Skip API calls (CSV only, requires companies & brands files)")
	print("  4) Dry run (no API calls, empty data structure scaffold)")
	while True:
		choice = input("Enter 1, 2 or 3: ").strip()
		if choice == "1":
			return "both"
		if choice == "2":
			if not companies_path.exists():
				print(f"companies file not found at {companies_path}; cannot run brands only.")
				continue
			return "brands"
		if choice == "3":
			missing = []
			if not companies_path.exists():
				missing.append(str(companies_path))
			if not brands_path.exists():
				missing.append(str(brands_path))
			if missing:
				print("Missing required files: " + ", ".join(missing))
				continue
			return "csv"
		if choice == "4":
			return "dry"
		print("Invalid selection. Please enter 1, 2 or 3.")


def main() -> int:
	"""Execute the workflow across all sections and store the combined output."""
	load_env()
	cfg = get_config()
	logger = configure_logger(level=logging.INFO)
	logger.info("Configuration loaded")
	client = create_client(cfg.api_key)
	logger.info(f"OpenAI client initialized (model={cfg.model})")
	start_time = time.time()
	companies_phase_start = None
	brands_phase_start = None
	flatten_phase_start = None
	companies_path = Path(cfg.companies_file)
	brands_path = Path(cfg.brands_file)
	mode = ask_run_mode(companies_path, brands_path)
	if mode == "dry":
		logger.info("Mode=dry: generating mock data (no API calls)")
		sections = load_sections(cfg.industries_file)
		companies_phase_start = time.time()
		section_responses = _collect_section_responses(
			client, cfg.model, sections, cfg.max_companies_per_industry, cfg.country, cfg.country_specific, logger, True
		)
		logger.info(f"Companies phase elapsed: {time.time() - companies_phase_start:.2f}s (dry run)")
		# Gather company names from mock data
		company_names = {
			entry.get("company_name")
			for company_list in section_responses.values()
			for entry in company_list
			if isinstance(entry, dict) and entry.get("company_name")
		}
		brands_phase_start = time.time()
		brands_data = _collect_brand_responses(
			client, cfg.model, sorted(company_names), cfg.max_brands_per_company, cfg.country, cfg.country_specific, logger, True
		)
		logger.info(f"Brands phase elapsed: {time.time() - brands_phase_start:.2f}s (dry run)")
		flatten_phase_start = time.time()
		flatten_to_csv(section_responses, brands_data, cfg.dataset_file)
		logger.info(f"Flatten phase elapsed: {time.time() - flatten_phase_start:.2f}s (dry run)")
		logger.info(f"Dry run complete. Mock dataset written to {cfg.dataset_file}")
		logger.info(f"Total elapsed: {time.time() - start_time:.2f}s")
		return 0
	if mode == "csv":
		# Load existing JSON artifacts only and regenerate CSV.
		logger.info("Mode=csv: loading existing JSON artifacts for CSV regeneration")
		section_responses = load_companies(str(companies_path))
		with brands_path.open("r", encoding="utf-8") as file:
			brands_data: dict[str, list[dict[str, str]]] = json.load(file)
		logger.info("Loaded brands JSON; writing CSV")
		flatten_phase_start = time.time()
		flatten_to_csv(section_responses, brands_data, cfg.dataset_file)
		logger.info(f"Flatten phase elapsed: {time.time() - flatten_phase_start:.2f}s")
		logger.info(f"CSV regenerated at {cfg.dataset_file}")
		return 0
	elif mode == "both":
		logger.info("Mode=both: loading sections and generating companies")
		sections = load_sections(cfg.industries_file)
		companies_phase_start = time.time()
		section_responses = _collect_section_responses(
			client, cfg.model, sections, cfg.max_companies_per_industry, cfg.country, cfg.country_specific, logger, False
		)
		logger.info(f"Companies phase elapsed: {time.time() - companies_phase_start:.2f}s")
		companies_path.parent.mkdir(parents=True, exist_ok=True)
		with companies_path.open("w", encoding="utf-8") as file:
			json.dump(section_responses, file, ensure_ascii=False, indent=2)
		logger.info(f"Saved companies JSON to {companies_path}")
	else:  # brands only
		logger.info("Mode=brands: loading existing companies JSON")
		section_responses = load_companies(str(companies_path))

	# Collect unique company names
	company_names = {
		entry.get("company_name")
		for company_list in section_responses.values()
		for entry in company_list
		if isinstance(entry, dict) and entry.get("company_name")
	}
	logger.info(f"Generating brands for {len(company_names)} unique companies")
	brands_phase_start = time.time()
	brands_data = _collect_brand_responses(
		client, cfg.model, sorted(company_names), cfg.max_brands_per_company, cfg.country, cfg.country_specific, logger, False
	)
	logger.info(f"Brands phase elapsed: {time.time() - brands_phase_start:.2f}s")
	brands_path.parent.mkdir(parents=True, exist_ok=True)
	with brands_path.open("w", encoding="utf-8") as file:
		json.dump(brands_data, file, ensure_ascii=False, indent=2)
	logger.info(f"Saved brands JSON to {brands_path}")
	flatten_phase_start = time.time()
	flatten_to_csv(section_responses, brands_data, cfg.dataset_file)
	logger.info(f"Flatten phase elapsed: {time.time() - flatten_phase_start:.2f}s")
	logger.info(f"Flattened dataset written to {cfg.dataset_file}")
	logger.info(f"Total elapsed: {time.time() - start_time:.2f}s")
	return 0


if __name__ == "__main__":  # pragma: no cover
	raise SystemExit(main())

