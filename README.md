# FERC + PJM Interconnection RAG

A retrieval-augmented generation (RAG) pipeline over FERC Order 2023 filings and PJM cluster study reports. Ask natural language questions like *"What are the most common reasons for restudy triggers?"* and get answers with citations back to the source PDF and page.

## Why this exists

The U.S. grid interconnection process is documented across thousands of fragmented PDFs — FERC orders, PJM cluster studies, RTO tariff filings. This is a small demo of unifying that corpus into a queryable knowledge base, the same problem space companies like Tapestry (Alphabet) work on at the operator level.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill in keys
```

Drop 10–20 source PDFs into `data/pdfs/`. Suggested seeds:

- FERC Order 2023 (docket RM22-14) — final rule + key NOPRs
- PJM cluster study reports from https://www.pjm.com/committees-and-groups/task-forces/cpstaff
- AD21-10 interconnection reform proceeding filings

## Run

```bash
# 1. Ingest PDFs into the vector store (idempotent — safe to re-run)
python -m src.ingest

# 2. Run the eval set against the pipeline
python -m src.eval

# 3. Launch the chat UI
streamlit run app.py
```

## Pipeline

```
PDFs -> chunked text (512 tok / 64 overlap) -> embeddings (OpenAI text-embedding-3-small)
     -> ChromaDB (persistent, local) -> retrieval (top-k) -> Claude Sonnet 4.6 -> answer + citations
```

## Project structure

```
ferc-pjm-rag/
  data/
    pdfs/               # raw source PDFs (gitignored)
    processed/          # chunked text cache (gitignored)
  src/
    ingest.py           # load, chunk, embed, persist
    query.py            # retrieve + generate with citations
    eval.py             # run a 10-question eval set
  app.py                # streamlit chat interface
  eval_set.json         # benchmark Q&A pairs
  .env.example          # required env vars
  README.md
```

## Eval set

10 hand-written questions covering FERC Order 2023, PJM cluster studies, deliverability, network upgrades, and queue mechanics. See `eval_set.json`. Use `src/eval.py` to run the set and inspect retrieved context + generated answers for manual review.

## Sources

- PJM interconnection process: https://www.pjm.com/planning/interconnection-projects
- FERC eLibrary: https://elibrary.ferc.gov/eLibrary/search (dockets RM22-14, AD21-10)
