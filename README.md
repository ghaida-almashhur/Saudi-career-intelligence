# Saudi Career Intelligence 🇸🇦

**An evidence-aware labor-market intelligence prototype for Saudi graduates.**

Instead of building another job-posting dashboard, this project asks a more useful question:

> **What career paths are realistically accessible to a fresh graduate, and what should they develop next?**

## Product

Saudi Career Intelligence combines real Jadarat job-posting data with official Saudi occupation and skills frameworks to provide:

- fresh-graduate market context;
- salary and experience analysis;
- a transparent Career Match prototype;
- a Fresh Graduate Opportunity Index (FGOI);
- official Data & AI occupation mapping;
- family-level Skill Coverage;
- a dedicated Statistics Graduate Pathway;
- a clearly labeled “What should I learn next?” prototype.

## Why this project is different

The project separates three kinds of evidence:

1. **Observed market data** — what appears in the available Jadarat datasets.
2. **Official evidence** — Saudi occupation / skills / career-family frameworks.
3. **Product heuristics** — transparent recommendation logic created for the prototype.

A heuristic is never presented as an official requirement, and a family-level skill is never presented as if every individual vacancy explicitly requested it.

## Architecture

`Raw Jadarat data → Python cleaning & feature engineering → SQLite/SQL → statistical models → official taxonomy layer → Streamlit product`

## Statistical work

### Fresh Graduate Opportunity Index v0.1
Combines entry accessibility, vacancy demand, salary attractiveness, geographic breadth and employer diversity. Component scores are percentile ranks.

The ranking was recalculated **3,000 times** under plausible weight perturbations to test whether conclusions depend heavily on one arbitrary set of weights.

### Salary model v0.1
A multivariable log-salary model controls for required experience, career family, city and organization size. Results are reported as **associations**, not causal effects.

## Tech stack

**Python · pandas · NumPy · SQL · SQLite · statistical modelling · Streamlit · Power BI-ready outputs**

## Repository map

- `app.py` — interactive MVP
- `data/raw/` — untouched source data
- `data/processed/` — reproducible analytical outputs
- `sql/` — schema and analytical queries
- `scripts/` — data-pipeline scripts
- `docs/` — methodology, QA, source registry, portfolio case study and deployment guide
- `saudi_career_intelligence.db` — analytical SQLite database

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Evidence & limitations

This is a portfolio research/product prototype, not a hiring-probability engine. Dataset coverage is not assumed to represent every Saudi vacancy. Official occupation matching is intentionally conservative. Skills are scoped to the level supported by the source. See `docs/sources_registry.csv`, `docs/data_quality_scorecard.csv`, and the methodology files for details.

## Next production milestone

Expand official occupation coverage, validate high-volume title mappings, integrate additional official labor-market data, and deploy the public MVP.

## Public repository note

Raw Jadarat files are not included in this public build pending verification of their redistribution terms.
Processed portfolio outputs are provided for demonstration; official Saudi framework evidence is attributed in `docs/sources_registry.csv`.

## Responsible use

This project is an independent portfolio prototype and is **not affiliated with or endorsed by HRSD or Jadarat**.
Scores are decision-support context, not hiring probabilities.
