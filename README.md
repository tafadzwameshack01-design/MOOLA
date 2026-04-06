# ⚽ ZEUS — Football Intelligence System

**Top 5 OVER 2.5 Goals picks from 35+ global leagues, every 5 minutes.**

---

## What it does

- Scans **35+ football leagues** worldwide (Premier League, La Liga, Bundesliga, Serie A, MLS, Brasileirão, and more)
- Filters only games **kicking off within the next 4 hours**
- Runs an **xG statistical model** on each game using real ESPN data (last 25 completed games per team)
- Returns the **top 5 highest-confidence OVER 2.5 goals picks**, sorted by confidence
- Auto-grades past picks once matches complete
- **No API keys required** — uses ESPN's free public soccer API

---

## Confidence tiers

| Tier | Range | Meaning |
|------|-------|---------|
| 🔥 ELITE | ≥72% | Exceptional edge — multiple strong signals all pointing OVER |
| ⚡ STRONG | 60–71% | Clear OVER signal with consistent historical data |
| ✅ CONFIDENT | <60% | Solid positive xG lean, less dominant but valid |

---

## Confidence model

The model combines 4 signals:

1. **xG Total (45%)** — Expected goals model:
   `xG_home = 0.55 × home_avg_scored + 0.45 × away_avg_conceded`
   `xG_away = 0.55 × away_avg_scored + 0.45 × home_avg_conceded`

2. **Historical OVER 2.5 Rate (40%)** — What % of each team's recent games went OVER 2.5

3. **Both Teams To Score Rate (10%)** — Proxy for open, attacking play

4. **Scoring Trend (5%)** — Are recent games higher-scoring than the season average?

Only games where `total_xG > 2.5` are considered for OVER picks.

---

## Deploy to Streamlit Cloud (free, always-on)

1. Create a new GitHub repository (e.g. `zeus-football`)
2. Upload both `app.py` and `requirements.txt` to the root of the repo
3. Go to [share.streamlit.io](https://share.streamlit.io)
4. Click **New app** → select your repo → main branch → `app.py`
5. Click **Deploy** — your app will be live in ~1 minute

> **Tip:** Streamlit Community Cloud is completely free and keeps your app online 24/7.

---

## File structure

```
zeus-football/
├── app.py            ← Main application
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

---

## Data source

All data comes from **ESPN's public soccer API** (no key required):
- `https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/scoreboard`
- `https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/teams/{id}/schedule`

Data is cached locally in SQLite to minimise API calls. Scoreboards refresh every 5 minutes, team schedules every hour.

---

*ZEUS is for informational purposes only. Always gamble responsibly.*
