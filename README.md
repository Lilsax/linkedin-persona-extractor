# linkedin-persona-extractor

Generates concise professional intros, highlights, interests, and tailored ice‑breakers for a person using LinkedIn data and an LLM backend. Ships a minimal Flask API you can run locally.

## Features

- Fetches LinkedIn profile data (BrightData or mock JSON)
- Produces JSON with summary, interesting facts, interests, ice‑breakers, and picture URL
- Switchable LLM backend (Google Generative AI or local Ollama)
- Flask API for quick integration

## Quick Start

1. Install dependencies (pipenv recommended):

```bash
pipenv install
```

2. Configure environment (copy and edit):

```bash
cp .env.example .env
```

Edit `.env` and set at least:

```
BRIGHT_DATA=your_brightdata_api_key   # required if using real scraping (mock=False)
GOOGLE_API_KEY=your_google_genai_key  # optional; falls back to local Ollama if not set
TAVILY_API_KEY=your_tavily_api_key    # required for LinkedIn URL search
# Optional overrides (safe defaults exist):
# MOCK_GIST_URL=...
# BRIGHTDATA_TRIGGER_URL=...
# BRIGHTDATA_SNAPSHOT_BASE=...
```

3. Run the API (example on port 8000):

```bash
PORT=8000 pipenv run python app.py
```

4. Call the endpoint:

```bash
curl 'http://127.0.0.1:8000/process?name=Jane%20Doe%20Software%20Engineer' | jq
```

## API

- GET `/process?name=<full name and title>`
  - Response JSON:
    - `summary_and_facts.summary`: one‑sentence intro
    - `summary_and_facts.facts`: two interesting facts
    - `interests`: list of interests
    - `ice_breakers`: three tailored ice‑breakers
    - `picture_url`: absolute URL (may be empty)

## Project Layout

- `app.py`: Flask entry with `/process` endpoint
- `introgen.py`: orchestration (LLM prompt/parse, JSON shaping)
- `agents/linkedinLookUpAgent.py`: finds the LinkedIn profile URL for a name
- `tools/tools.py`: Tavily search tool (biases queries to LinkedIn)
- `thirdparties/linkedin.py`: LinkedIn data fetch via BrightData or mock

## Notes

- LLM backend: If `GOOGLE_API_KEY` is not set, the code uses `llama3` via Ollama. Ensure Ollama is running locally with that model installed.
- Scraping: Real scraping requires `BRIGHT_DATA`. For development, you can adapt code paths to use `mock=True` to avoid network calls.
- Keep your `.env` out of version control (already in `.gitignore`).
