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
| **Spotify Mood Ring** ⭐ | Analyzes your last 30 days of Spotify listening and generates a "mood report" with a custom AI-written playlist description | Spotify API + LLM + data viz — shareable social content |
| **Receipt Roast** | Scan a grocery/restaurant receipt and get a brutally honest AI breakdown of your food choices ("7 energy drinks and no vegetables") | OCR + LLM pipeline, hilarious demo project |
| **Bracket Builder for Everything** | March-Madness-style bracket generator for anything — movies, foods, travel destinations — with shareable links | Timely, social, and a clean full-stack build |
| **Noise Complaint Heatmap** | Pull public 311 noise complaint data and overlay it on a map — find the loudest block in your city | Real public data, maps, satisfying to explore |
| **Tech Job Title Translator** | Paste a confusing job description and get a plain-English summary of what you'd actually do day-to-day | LLM + humor, genuinely useful, very shareable |
| **Commit Message Roaster** | GitHub Action that reviews your commit history and rates message quality with a running "commit hygiene score" | Developer humor, CI/CD, practical tool |
| **"Would You Rather" for Career Decisions** | AI-powered career decision helper — weigh job offers, cities, life choices — outputs a structured pros/cons breakdown | Combines LLM reasoning with real decision fatigue people feel |
| **Vibe Photo → Playlist** | Take a photo of your surroundings and get a Spotify playlist that matches the mood/aesthetic | Vision API + Spotify API — instant, shareable, zero friction |
| **Am I Being Ghosted?** | Paste a text thread, AI gives you a ghosting probability score and a brutally honest read of the situation | LLM + dark humor, insanely shareable |
| **Side Hustle ROI Calculator** | Input your hours, expenses, and revenue from any side project — get an honest "is this worth it?" breakdown | Actually useful, hits close to home with CAMUVA background |
| **Bar Trivia Generator** | Generate a full custom trivia night from any topic, with a host mode and per-team scoring | Great for real-world use, fun to demo live |
| **Sleep Score from Screen Time** | Pull iOS Screen Time data and correlate app usage patterns with self-reported sleep quality over time | Health data + ML, personal and relatable |

---

## Spotlight: Spotify Mood Ring — Mobile Build Plan

> Build a mobile PWA (no app store required) that reads your Spotify listening history and generates a shareable AI mood report.

### How it works

1. User taps "Connect Spotify" → OAuth login via Spotify
2. App fetches last 30 days of top tracks + audio features (energy, valence, tempo, danceability)
3. Aggregates genre distribution and listening time-of-day patterns
4. Sends summary to Claude API → generates a narrative mood description + a custom playlist name
5. Renders a shareable "mood card" (like a Spotify Wrapped card) the user can screenshot or share

### Tech stack

| Layer | Choice | Why |
|---|---|---|
| **Frontend** | React (Vite) — mobile-optimized PWA | Installable from Safari/Chrome, no App Store |
| **Backend** | FastAPI (Python) | Lightweight, async, easy Spotify + Claude API calls |
| **Auth** | Spotify OAuth 2.0 (PKCE flow) | No backend secret needed — works purely client-side if desired |
| **AI** | Claude API (`claude-sonnet-4-6`) | Narrative mood generation from structured listening data |
| **Hosting** | Render (backend) + Vercel (frontend) | Both free tiers, auto-deploy from GitHub |
| **Shareable card** | `html2canvas` or `dom-to-image` | Screenshot the mood card div → download as PNG |

### File structure

```
spotify-mood-ring/
├── backend/
│   ├── main.py              ← FastAPI app, Spotify + Claude API calls
│   ├── spotify.py           ← Fetch top tracks, audio features, genres
│   ├── mood.py              ← Build Claude prompt, parse response
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx          ← Route: /login, /loading, /results
│   │   ├── SpotifyLogin.jsx ← OAuth PKCE initiation
│   │   ├── MoodCard.jsx     ← The shareable results card
│   │   └── api.js           ← Calls to FastAPI backend
│   ├── public/
│   │   └── manifest.json    ← PWA manifest (installable on home screen)
│   └── vite.config.js
└── README.md
```

### Claude prompt design

```
You are a music psychologist. Based on this person's Spotify listening data
from the past 30 days, write a 3-4 sentence "mood report" in a witty,
insightful tone. End with a custom playlist name that captures their vibe.

Data:
- Top genres: {genres}
- Average energy: {energy}/1.0
- Average valence (happiness): {valence}/1.0
- Peak listening time: {peak_hour}:00
- Most played artist: {top_artist}
- Total tracks analyzed: {track_count}
```

### Build order (weekend sprints)

- [ ] **Sprint 1** — Spotify OAuth + fetch listening data, log it to console
- [ ] **Sprint 2** — FastAPI backend, Claude mood generation, test with Postman
- [ ] **Sprint 3** — React frontend, mobile layout, connect to backend
- [ ] **Sprint 4** — Mood card UI, share/download button, PWA manifest
- [ ] **Sprint 5** — Deploy to Vercel + Render, add to portfolio

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
