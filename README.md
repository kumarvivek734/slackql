# SlackQL — AI Data Analyst for Slack

**Ask questions in plain English. Get SQL-powered answers in Slack.**

SlackQL is an open-source Slack bot that lets your team query databases using natural language. Powered by Gemini AI, it translates questions like *"What were our top 5 products by revenue last month?"* into SQL, executes them safely, and returns formatted results — all within Slack.

---

## Problem

- Business teams depend on data analysts for every ad-hoc query
- Simple questions like "how many orders yesterday?" take hours to get answered
- Non-technical stakeholders can't write SQL

## Solution

SlackQL bridges the gap:

1. User asks a question in a Slack channel (e.g., `/ask What's our daily revenue trend this week?`)
2. AI translates the question to SQL using your database schema as context
3. Query runs against your database (read-only, with guardrails)
4. Results are formatted and posted back to Slack — as a table, summary, or chart

---

## Architecture

```
┌─────────┐     ┌────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  Slack   │────▶│ Slack Bolt │────▶│  Gemini AI   │────▶│ Guardrails  │────▶│ PostgreSQL   │
│ /ask cmd │◀────│  (Python)  │     │ (Text → SQL) │     │ - Read-only │     │ (Read-only)  │
└─────────┘     └────────────┘     └──────────────┘     │ - Timeout   │     └──────────────┘
▲                                 │ - Row limit │            │
│                                 │ - DML block │            │
│                                 └─────────────┘            │
│                                                            │
└────────────────── Response ◀───────────────────────────────┘

```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Bot Framework | Slack Bolt (Python) |
| AI Engine | Gemini API |
| Database | PostgreSQL (any SQL DB supported) |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Slack workspace (admin access)
- Gemini API key
- PostgreSQL database

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/slackql.git
cd slackql
cp .env.example .env
# Edit .env with your credentials
```

### 2. Run with Docker Compose
```bash
docker compose up --build -d
```
This starts two containers: the SlackQL bot and a PostgreSQL database preloaded with a demo e-commerce dataset (customers, products, orders, order_items).

### 3. Configure Slack App
See slack docs [https://api.slack.com/apps] for step-by-step Slack app configuration.

### 4. Try it
In any Slack channel where the bot is invited:
```
/ask How many orders were placed yesterday?
/ask What are the top 5 customers by total spend?
/ask Show me daily revenue for the last 7 days
```

## 📁 Project Structure

```
slacksql/
├── app/
│   ├── bot/          # Slack Bolt event handlers
│   ├── llm/          # Gemini AI integration & prompt engineering
│   ├── db/           # Database connection & query execution
│   ├── config.py     # App configuration (Pydantic Settings)
│   └── main.py       # Entry point
├── seed/             # Demo database (SQL + CSV)
├── tests/            # Unit & integration tests
├── dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Safety & Guardrails

- **Read-only access**: Bot uses a read-only database user — no writes, deletes, or DDL
- **Row limits**: Results capped at 100 rows to prevent Slack message overflow
- **Query timeout**: 10-second timeout on all queries
- **Schema-aware**: AI only generates queries against known tables/columns
- **Audit log**: Every question, generated SQL, and result is logged

MIT License — see [LICENSE](LICENSE)

