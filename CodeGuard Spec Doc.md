# CodeGuard: AI-Powered PR Review Assistant

An AI-powered GitHub bot that automatically reviews pull requests for code quality, security, and documentation issues.

## Project Structure

```
codeguard/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── models/         # Database models & schemas
│   │   ├── routers/        # API endpoints
│   │   ├── services/       # Business logic (GitHub, Claude)
│   │   └── utils/          # Helpers & prompts
│   └── requirements.txt
├── frontend/               # React dashboard
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom React hooks
│   │   └── api/            # API client
│   └── package.json
├── .env.example            # Environment variables template
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Anthropic API key
- GitHub Personal Access Token (or GitHub App)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy environment template and add your keys
cp ../.env.example ../.env
# Edit .env with your API keys

# Run the server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The dashboard will be available at http://localhost:3000

### Testing with ngrok (for GitHub webhooks)

```bash
ngrok http 8000
```

Use the ngrok URL as your GitHub webhook endpoint.

## Environment Variables

Copy `.env.example` to `.env` and fill in:

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `GITHUB_TOKEN` | GitHub Personal Access Token |
| `GITHUB_WEBHOOK_SECRET` | Secret for webhook validation |

## Features

- **Automated PR Analysis**: Analyzes code changes using Claude AI
- **Inline Comments**: Posts contextual feedback on specific lines
- **Learning Mode**: Adapts to team preferences over time
- **Metrics Dashboard**: Track issues, trends, and time saved

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/webhook/github` | POST | GitHub webhook receiver |
| `/api/analysis/{id}` | GET | Get analysis results |
| `/api/metrics` | GET | Dashboard metrics |

## License

MIT
