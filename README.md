# Cameron J. Davis — Portfolio

Personal portfolio website built with Django. Displays a gallery of projects with images and summaries.

---

## Project Ideas

A running list of personal project ideas that fit Cameron's background in cloud security, AI, full-stack engineering, and entrepreneurship.

### Tier 1 — High signal, on-brand

| Project | Description | Why it fits |
|---|---|---|
| **IAM Policy Linter** | CLI that scans AWS/GCP/IBM Cloud IAM policies, flags overprivileged roles, and suggests tighter rules | 2.5 years on IAM & Context Based Restrictions at IBM — deep expertise, real open-source gap |
| **Compliance RAG Chatbot** | Point an LLM at a regulatory doc (SOC 2, HIPAA, FedRAMP) and ask compliance questions via retrieval-augmented generation | Bridges IBM compliance tooling + IBM AI Cloud Assistant + Artium AI |
| **Zero-Trust Policy Visualizer** | Parse CBR/network policy configs (JSON/YAML) into an interactive graph showing which services can talk to which | Visual tooling for this space barely exists — unique and demonstrable |

### Tier 2 — Entrepreneurial / practical

| Project | Description | Why it fits |
|---|---|---|
| **CAMUVA V2** | Mobile-first booking app for the repair business — job intake, status tracking, Stripe payments | Turns entrepreneurship into engineering; Stripe is already in requirements.txt |
| **Personal Finance Dashboard** | Pull bank/credit data via Plaid, auto-categorize with ML, visualize trends | Pandas + TensorFlow + Django all in one project |

### Tier 3 — AI tooling

| Project | Description | Why it fits |
|---|---|---|
| **PR Review Agent** | GitHub bot that reviews pull requests against a configurable ruleset (style, security anti-patterns, complexity) using an LLM | Directly aligned with Artium AI's human-AI collaboration focus |
| **Local LLM Benchmark Dashboard** | Run the same prompts across local models (Ollama etc.), track response quality, speed, and cost over time | Scratches a real itch for engineers choosing models |

### Fun / wild card ideas

| Project | Description | Why it's fun |
|---|---|---|
| **GeoGuesser for Campuses** | Street-view-style guessing game but for college campuses — drop into a random campus photo and guess which school | Multiplayer concept, Google Street View API + leaderboard |
| **Spotify Mood Ring** | Analyzes your last 30 days of Spotify listening and generates a "mood report" with a custom AI-written playlist description | Spotify API + LLM + data viz — shareable social content |
| **Receipt Roast** | Scan a grocery/restaurant receipt and get a brutally honest AI breakdown of your food choices ("7 energy drinks and no vegetables") | OCR + LLM pipeline, hilarious demo project |
| **Bracket Builder for Everything** | March-Madness-style bracket generator for anything — movies, foods, travel destinations — with shareable links | Timely, social, and a clean full-stack build |
| **Noise Complaint Heatmap** | Pull public 311 noise complaint data and overlay it on a map — find the loudest block in your city | Real public data, maps, satisfying to explore |
| **Tech Job Title Translator** | Paste a confusing job description and get a plain-English summary of what you'd actually do day-to-day | LLM + humor, genuinely useful, very shareable |
| **Commit Message Roaster** | GitHub Action that reviews your commit history and rates message quality with a running "commit hygiene score" | Developer humor, CI/CD, practical tool |
| **"Would You Rather" for Career Decisions** | AI-powered career decision helper — weigh job offers, cities, life choices — outputs a structured pros/cons breakdown | Combines LLM reasoning with real decision fatigue people feel |

---

## Running the App Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the dev server
python manage.py runserver
```

Visit `http://127.0.0.1:8000`
