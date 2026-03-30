# CodeGuard AI

> Autonomous PR review powered by Claude — catches security vulnerabilities, code quality issues, and missing documentation before they hit your main branch.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Claude API](https://img.shields.io/badge/Claude-AI%20Powered-CC785C?style=flat)](https://anthropic.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-Dashboard-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](LICENSE)

---

## What It Does

CodeGuard integrates directly into your GitHub workflow via webhooks. When a PR is opened or updated, it automatically:

1. **Pulls the diff** from the GitHub API
2. **Sends it to Claude** with a structured prompt targeting security, quality, and documentation gaps
3. **Posts inline comments** on specific lines — just like a human reviewer
4. **Logs results** to a React dashboard with trends and metrics over time

No manual steps. No context switching. Engineers get AI feedback within seconds of opening a PR.

---

## Architecture

```
GitHub PR Event
      │
      ▼
GitHub Webhook ──► FastAPI Backend ──► Claude API (Anthropic)
                        │                      │
                        │              Structured Analysis
                        │              (security · quality · docs)
                        ▼                      │
                   PostgreSQL ◄────────────────┘
                        │
                        ▼
                 React Dashboard
              (metrics · trends · history)
```

**Stack:**
- **Backend**: FastAPI (Python 3.11) — webhook receiver, GitHub API client, Claude integration
- **AI**: Claude API — diff analysis with structured prompts targeting specific review categories
- **Frontend**: React — metrics dashboard showing issues caught, time saved, trend analysis
- **Webhooks**: GitHub webhook events + ngrok for local development

---

## Key Features

**Automated PR Analysis**
Claude reviews every diff for security vulnerabilities, logic errors, missing error handling, and code smells — with inline comments on specific lines, not generic summaries.

**Security-Focused Prompting**
Prompts are structured to surface high-severity issues first: hardcoded secrets, SQL injection risks, unvalidated inputs, and dependency issues.

**Metrics Dashboard**
Track issues caught per PR, categories over time, and estimated review hours saved. Useful for demonstrating DevEx ROI.

**Webhook-Driven**
Fully event-driven — no polling, no manual triggers. Works with any GitHub repo via webhook configuration.

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Anthropic API key ([get one here](https://console.anthropic.com))
- GitHub Personal Access Token with `repo` scope

### 1. Clone & Configure

```bash
git clone https://github.com/fayad-abbasi/codeguard-ai.git
cd codeguard-ai
cp .env.example .env
```

Edit `.env` with your credentials:

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `GITHUB_TOKEN` | GitHub PAT with `repo` scope |
| `GITHUB_WEBHOOK_SECRET` | Secret string for webhook validation |

### 2. Start the Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Start the Frontend

```bash
cd frontend
npm install
npm run dev
# Dashboard at http://localhost:3000
```

### 4. Expose Webhook (Local Dev)

```bash
ngrok http 8000
# Copy the HTTPS URL → use as your GitHub webhook endpoint
```

In your GitHub repo: **Settings → Webhooks → Add webhook**
- Payload URL: `https://your-ngrok-url/webhook/github`
- Content type: `application/json`
- Events: `Pull requests`

---

## API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/webhook/github` | `POST` | GitHub webhook receiver — triggers PR analysis |
| `/api/analysis/{id}` | `GET` | Retrieve analysis results for a specific PR |
| `/api/metrics` | `GET` | Aggregate metrics for the dashboard |

---

## Project Structure

```
codeguard-ai/
├── backend/
│   ├── app/
│   │   ├── models/         # Database models & schemas
│   │   ├── routers/        # API endpoints
│   │   ├── services/       # GitHub API + Claude integration
│   │   └── utils/          # Prompt templates & helpers
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Dashboard pages
│   │   ├── hooks/          # Custom React hooks
│   │   └── api/            # Backend API client
│   └── package.json
└── .env.example
```

---

## Why I Built This

As a DevEx PM, I wanted to understand the full stack of an AI-powered developer tool — not just the product decisions, but the webhook plumbing, prompt engineering, and API integration that makes it work. CodeGuard is that project: a real tool I use to explore how AI can reduce reviewer fatigue and catch issues earlier in the SDLC.

The bigger question I'm exploring: **what does it look like when AI becomes a first-class participant in the development workflow**, not just an autocomplete engine?

---

## Roadmap

- [ ] GitHub App (vs. PAT) for easier multi-repo deployment
- [ ] Configurable review profiles (security-heavy, docs-focused, etc.)
- [ ] PR comment threading — respond to CodeGuard comments to refine analysis
- [ ] Slack/Teams notifications for high-severity findings
- [ ] Fine-tuning prompts per team coding standards

---

## Related Projects

- [ai-podcast-generator](https://github.com/fayad-abbasi/ai-podcast-generator) — Claude-powered audio summaries from any content source
- [OpenClaw (Privacy-First)](https://github.com/fayad-abbasi/My-privacy-first-OpenClaw-Implementation) — Self-hosted AI assistant on Raspberry Pi

---

## License

MIT — use it, fork it, build on it.

---

<div align="center">
  <sub>Built by <a href="https://linkedin.com/in/fayad-abbasi">Fayad Abbasi</a> · DevEx PM exploring the edges of AI developer tooling</sub>
</div>
