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

### Extending / API Usage

Minimal example using the package programmatically:
```python
from brandgen import (
	load_env, get_config, create_client,
	build_prompt, build_companies_prompt, ask_companies
)

load_env()
cfg = get_config()
client = create_client(cfg.api_key)
prompt = build_prompt(build_companies_prompt("Manufacturing", cfg.country, cfg.country_specific))
companies = ask_companies(client, cfg.model, prompt)
print(len(companies))
```

Customize prompts via `prompt.py` constants; adjust breadth with `MAX_*` env vars; extend
CSV shape by editing `brandgen/flatten.py`.

### Reliability & Validation

- Required environment variables validated at startup.
- Structured responses enforced using OpenAI `json_schema` format.
- Deterministic(ish) output encouraged via low temperature (0.2).

### Versioning & Dependencies

Dependencies pinned with upper bounds in `requirements.txt` for reproducibility.

### License

Released under the MIT License. See `LICENSE` for details.

