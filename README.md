## Brands & Companies Dataset Generator

Structured synthetic data generator for companies and their brands / products / services
across ISIC Rev.4 industry sections. The pipeline:

1. Iterate ISIC sections and generate company objects (name, HQ country, activities).
2. For each company generate brand / product / service records with GPC taxonomy.
3. Flatten nested JSON into a single analytics‑ready CSV.

Now modularized via the internal `brandgen` package for clarity and reuse.

### Setup

1. Create a virtual environment (recommended)
```
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Configure environment variables
```
copy config\.env.example config\.env
# Edit config\.env and add your actual OPENAI_API_KEY
```

### Usage (CLI)

Run the orchestrator and pick a mode:
```
python generate.py
```
Menu options:
1) Full run (companies then brands then CSV)
2) Brands only (reuse existing companies JSON)
3) CSV only (reuse existing companies & brands JSON)

Outputs written to `data/` (paths configurable via env):
- Companies JSON (`COMPANIES_FILE`) — dict: section label -> list[company]
- Brands JSON (`BRANDS_FILE`) — dict: company name -> list[brand]
- Flattened CSV (`DATASET_FILE`)

### Package Structure

```
brandgen/
	__init__.py          # Public exports
	api.py               # OpenAI client + schema calls
	config.py            # Env & typed configuration
	schemas.py           # JSON schema definitions
	prompt_builder.py    # Prompt assembly utilities
	persist.py           # Load/save JSON & sections
	flatten.py           # CSV export logic
 	prompt.py            # Prompt template constants (global + country variants)
generate.py            # CLI / orchestration
```

`generate.py` imports only from `brandgen` for a narrow surface area; you can also
import `brandgen` in your own scripts to build custom workflows.

### Environment Variables (`config/.env`)
```
OPENAI_API_KEY=sk-...
GPT_MODEL=gpt-4o
INDUSTRIES_FILE=data/industries.json
COMPANIES_FILE=data/companies.json
BRANDS_FILE=data/brands.json
DATASET_FILE=data/dataset.csv
# Optional caps (0 = unlimited)
MAX_COMPANIES_PER_INDUSTRY=10
MAX_BRANDS_PER_COMPANY=15
COUNTRY=United States
COUNTRY_SPECIFIC=True
```

If limits are set (>0) lists are truncated after the API response, reducing token usage and CSV size. If `COUNTRY_SPECIFIC` is true and `COUNTRY` is non-empty, country-scoped templates are used; otherwise global templates are used.

### Versioning & Dependencies

Dependencies pinned with upper bounds in `requirements.txt` for reproducibility.

### Data Sources

#### Wikidata
The project includes utilities for collecting company and brand data from Wikidata:
- SPARQL queries to extract structured company information
- Resulting CSV datasets with company classifications and metadata
- Located in `data/` directory

#### ISIC Classification
The project uses the ISIC Rev.5 standard for industry classification:
- **Source**: `data/isic/ISIC5_Exp_Notes_11Mar2024.xlsx` - Official ISIC Rev.5 explanatory notes
- **Flattening Script**: `scripts/flatten_isic.py` - Converts hierarchical Excel structure to flat CSV
- **Output**: `data/isic/ISIC5_Exp_Notes_11Mar2024_flattened.csv` - Analytics-ready format with columns:
  - `section_name`, `division_name`, `group_name`, `class_name`
  - `includes`, `excludes` - Activity descriptions and exclusions

To regenerate the flattened ISIC data:
```
python scripts/flatten_isic.py
```

### ISIC Sections
When using level 1 (sections) in the environment configuration, the system uses ISIC Rev.4 sections from `data/industries.json`. For more detailed classifications, use the ISIC Rev.5 data described in the Data Sources section above.

### Regional Brand References
- **Egyptian Brands**: See `Egyptian_Brands.md` for a comprehensive source table of Egyptian business directories, government registries, brand databases, and APIs for collecting Egyptian company and brand data

### Logging & Resume Capability

The generator supports durable progress and resumable runs:

Environment additions (optional):
```
LOG_FILE=logs/run.log          # If set, all console logs also written to this file
STARTING_ISIC_LEVEL=1          # 1 = sections, 3 = ISIC groups (Rev.5 flattened)
ISIC_FLATTENED_FILE=data/isic/ISIC5_Exp_Notes_11Mar2024_flattened.csv
```

Run modes now include a fifth option:
```
5) Resume (continue from any partially generated companies / brands JSON)
```

How it works:
- Companies and brands are written incrementally after each successful API call (atomic temp -> final file).
- If the process stops (network error, CTRL+C), choose mode 5 to continue without re-querying completed entries.
- Partial companies file: already generated sections/groups are skipped.
- Partial brands file: already generated companies are skipped.

Tips:
- You can lower `MAX_COMPANIES_PER_INDUSTRY` / `MAX_BRANDS_PER_COMPANY` to test quickly, then resume with larger limits (new entries added for untouched sections/companies only).
- Logs accumulate in `LOG_FILE`; rotate manually if desired.

Failure recovery sequence:
1. Investigate last lines in `logs/run.log` (or console) for the failure origin.
2. Fix configuration or connectivity.
3. Re-run `python generate.py` and pick option 5 (Resume).

All JSON writes are atomic to prevent corruption on interruption.

### License

Released under the MIT License. See `LICENSE` for details.

