# FERC + PJM Interconnection RAG

A retrieval-augmented generation pipeline over the regulatory and operator documents that govern how new generation connects to the U.S. grid. Ask natural-language questions like *"What financial milestones must developers meet to maintain queue position?"* and get an answer with citations back to the source PDF and page.

Companion to [`interconnection-queue-analysis`](https://github.com/keanuhea/interconnection-queue-analysis) — the structured-data simulation side of the same problem. Together: two angles on the fragmented-data problem Tapestry (Alphabet) is solving for grid operators.

## Why this exists

The interconnection process is governed by documents — FERC Order 2023, the rehearing order, PJM's tariff manuals, individual cluster study reports — that live as un-queryable PDFs scattered across regulatory and operator sites. A planner who wants to know "how does Order 2023-A change cost allocation in clusters?" reads through hundreds of pages. This dashboard is a small demo of what changes when you put a retrieval-augmented model on top of that corpus.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Indexing is free** — embeddings run locally via `BAAI/bge-small-en-v1.5` (downloaded on first run, ~130 MB). **Querying needs an Anthropic API key** for Claude generation:

```bash
cp .env.example .env
# edit .env and add ANTHROPIC_API_KEY=sk-ant-...
```

## Run

```bash
# Index the corpus (free — local embeddings)
python -m src.ingest

# Run the eval set against the pipeline (~$0.05 in API calls)
python -m src.eval

# Launch the chat dashboard
streamlit run app.py
```

## Pipeline

```
PDFs (5 docs, ~600 pages)
  │
  ▼
SentenceSplitter (512 tok / 64 overlap)
  │
  ▼
HuggingFace BAAI/bge-small-en-v1.5  ← runs locally, no API
  │
  ▼
ChromaDB (persistent, on disk)
  │
  ▼
Top-k retrieval (k=5)
  │
  ▼
Claude Sonnet 4.6 ← only API call, only at query time
  │
  ▼
Answer + citations (filename + page + similarity score)
```

## Seed corpus

5 documents currently indexed (download targets in `src/ingest.py`):

| Document | Source | Why |
|---|---|---|
| FERC Order 2023 (final rule, 336 pp) | govinfo.gov | The reform that mandated cluster studies |
| FERC Order 2023-A (rehearing, 238 pp) | govinfo.gov | Clarifications and amendments |
| PJM Interconnection Reform Progress | pjm.com | Operator's status as of 2025 |
| PJM Generation Interconnection (fact sheet) | pjm.com | The high-level operator view |
| PJM Facility Study (queue AB1-092) | pjm.com | A real per-project study, for grounding |

The corpus is intentionally small for portfolio purposes. The pipeline is set up to scale to 100+ documents without code changes — re-run `python -m src.ingest` after dropping new PDFs in `data/pdfs/`.

## Project structure

```
ferc-pjm-rag/
  data/
    pdfs/               # source PDFs (gitignored)
  src/
    config.py           # paths, model names, LlamaIndex Settings
    ingest.py           # load, chunk, embed, persist (no API needed)
    query.py            # retrieve + generate with citations
    eval.py             # run the 10-question eval set
  app.py                # Streamlit dashboard
  eval_set.json         # benchmark Q&A pairs
  .env.example
  README.md
```

## Eval set

10 hand-written questions covering Order 2023, cluster studies, deliverability, network upgrades, and queue mechanics. See `eval_set.json`. Use `src/eval.py` to run the set and inspect retrieved context + generated answers.

## Sources

- FERC eLibrary: https://elibrary.ferc.gov/eLibrary/search (dockets RM22-14, RM22-14-001)
- Federal Register / govinfo.gov mirrors of the published orders
- PJM interconnection process: https://www.pjm.com/planning/interconnection-projects
