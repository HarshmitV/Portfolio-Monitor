# AI Infrastructure Coverage Universe Monitor

A systematic monitoring and research platform for an AI infrastructure 
coverage universe. NOT a personal portfolio tracker.

## What this project is

This is a coverage universe research tool — the kind of system a junior 
buyside analyst might build to systematize their thinking across a vertical 
specialization. It monitors 8-12 AI infrastructure positions across the 
stack (merchant compute, custom silicon, foundry, networking, data center 
infrastructure, data infrastructure software, enterprise AI applications, 
and neoclouds), runs compound-condition alerts against them, surfaces 
upcoming catalysts with thesis context, and (in later phases) benchmarks 
holdings against M&A precedent transactions and backtests the systematic 
exit framework.

## What this project is NOT

- A personal portfolio tracker
- A P&L calculator
- A trading tool

Positions in this system are research positions, not owned positions. 
Most are watchlist (shares = irrelevant), some may correspond to real 
holdings but the project does not track them as such.

## Important context about me

I am a beginner programmer with CS fundamentals (DSA) but limited 
practical building experience. I am also a finance-track undergrad at 
Brown, focused on AI infrastructure as a vertical specialization for 
tech IB recruiting (TMT groups).

Working style I prefer:
- Always propose a plan in plain English before writing code, and wait 
  for me to approve
- When you write code, explain what each new function or file does and why
- Prefer simple, readable code over clever or short code
- If I seem confused, slow down and explain — I'd rather build slowly 
  and understand than build fast and not
- When I push back on something, engage with the substance rather than 
  immediately capitulating; the disagreement is often where learning lives

## Data model conventions

**Positions do NOT have:**
- `shares` (positions are research positions, not owned)
- `cost_basis` (nothing was purchased)
- Anything related to portfolio P&L

**Positions DO have:**
- `ticker` — stock symbol
- `coverage_start_date` — when I began researching (NOT when I bought)
- `purpose` — usually `"watchlist"`
- `coverage_depth` — one of `"deep"`, `"moderate"`, `"surface"` — 
  encodes how much research I've done
- `thesis_direction` — one of `"long"`, `"short"`, `"neutral_monitor"` — 
  encodes my analytical view
- `sub_sector` — taxonomy label (see below)
- `sector_etf` — benchmark ETF for sector-relative alerts
- `peer_basket` — list of competitor tickers for peer-relative alerts
- `thesis` — written investment thesis
- `thesis_metrics` — dict of metric name to threshold, suffix `_min` 
  or `_max` indicates direction
- `target_price` — intrinsic value estimate
- `valuation_method` — how the target was derived
- `bear_triggers` — qualitative events that would invalidate the thesis
- `precedent_acquirers` — plausible strategic acquirers (for Phase 3 M&A signals)
- `alerts` — list of structured compound alert configurations

## Sub-sector taxonomy (use consistently)

- `ai_compute_merchant_silicon` — NVDA, AMD
- `ai_compute_custom_silicon` — AVGO, MRVL
- `ai_compute_foundry` — TSM
- `ai_networking` — ANET
- `ai_data_center_infrastructure` — VRT
- `ai_data_center_reit` — DLR, EQIX
- `ai_data_infrastructure` — SNOW, MDB
- `ai_enterprise_applications` — PLTR
- `ai_neocloud` — CRWV, NBIS

## Short-thesis alert sentiment inversion

For positions with `thesis_direction: "short"` (like CRWV in our universe), 
alert sentiment inverts:
- Weakness alerts (price drop, etc.) are labeled `"sentiment": "bullish"` 
  because they confirm the short thesis
- Strength alerts (price rally, etc.) are labeled `"sentiment": "bearish"` 
  because they put the short thesis at risk

The engine itself doesn't enforce this — the alert configurations in 
holdings.json encode the right sentiment per position. The engine just 
needs to pass sentiment through to the Discord embed color.

## Language to use in code, comments, output

Use:
- "coverage universe" (not "portfolio")
- "covered names" or "coverage positions" (not "holdings" or "positions you own")
- "performance since coverage start" (not "gain/loss")
- "monitoring conditions" or "research signals" (not "trading signals")
- "thesis cards" or "analytical write-ups" (not "position notes")

Avoid:
- "Your portfolio is worth X" — coverage tools don't compute portfolio value
- "Total P&L" — coverage tools don't track personal P&L
- "Your investments" — coverage tools track research positions, not investments

The file name `holdings.json` can stay for code continuity, but the 
summary header and user-facing output should reflect coverage / research 
framing.

## Stack

- Python 3.11+
- yfinance for prices and volumes (basic data)
- Financial Modeling Prep (FMP) for fundamentals (Phase 2 onward)
- JSON files for config and state (no database)
- Discord webhook for alerts
- GitHub Actions for cloud scheduling (Phase 1 Day 5 onward)
- Anthropic API for LLM-powered earnings analysis (Phase 3 Day 15 onward)

## Architecture conventions

- **Registry pattern** for condition types: each compound-alert condition 
  is a function registered in a dict (`CONDITION_REGISTRY`) under a 
  string key. The evaluator looks up the function by name. New condition 
  types are added by writing a new function and registering it — the 
  evaluator never changes.
- **Centralized market data fetching**: a `market_data.py` module 
  batch-fetches all needed price/volume/ETF data once per cycle and 
  passes it to all conditions, rather than each condition fetching 
  separately.
- **Separation of state from logic**: alert state lives in 
  `alert_state.json` (gitignored), distinct from configuration in 
  `holdings.json`.
- **Schema versioning**: `holdings.json` has a `schema_version` field at 
  the top so future migrations are explicit.

## Goal of this project

Build a serious, defensible piece of work that demonstrates:
1. Software engineering competence (registry pattern, state management, 
   cloud deployment)
2. Investment process maturity (thesis-driven monitoring, M&A precedent 
   benchmarking, backtesting with methodological honesty)
3. Vertical specialization in AI infrastructure (coverage universe spans 
   the full stack, thesis cards reflect genuine sub-sector analysis)
4. AI-and-finance fluency (LLM-powered earnings analysis integrated into 
   monitoring workflow)

The artifact should be resume-worthy for tech IB recruiting (TMT groups), 
with a public GitHub repo, working live system, and a published blog post 
documenting the methodology and backtest results.