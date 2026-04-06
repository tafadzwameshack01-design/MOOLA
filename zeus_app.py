"""
╔══════════════════════════════════════════════════════════════╗
║          ZEUS ⚽ FOOTBALL INTELLIGENCE SYSTEM v1.0           ║
║   OVER 2.5 Goals · Top 5 World Picks · 4-Hour Window        ║
║   Scans 35+ Global Leagues · Real-Time · Free APIs Only     ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import streamlit.components.v1 as components
import requests
import sqlite3
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple, Any
import time
import hashlib

# ── MUST be first Streamlit call ────────────────────────────────
st.set_page_config(
    page_title="ZEUS ⚽ Football Intelligence",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": "ZEUS Football Intelligence — Top 5 OVER 2.5 Picks from 35+ world leagues."}
)

# ══════════════════════════════════════════════════════════════
#  CSS — Stadium-at-Night aesthetic
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@400;500&display=swap');

:root {
  --bg:       #060c06;
  --surface:  #0c180c;
  --card:     #0f1e0f;
  --border:   #1c3a1c;
  --green:    #39ff14;
  --green2:   #00c853;
  --gold:     #ffb300;
  --gold2:    #ff8f00;
  --text:     #d4f0d4;
  --muted:    #5a8a5a;
  --red:      #ff1744;
}

html, body, .stApp {
  background: var(--bg) !important;
  font-family: 'Barlow', sans-serif;
}

/* Animated pitch-line background */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(57,255,20,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(57,255,20,0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  animation: gridMove 20s linear infinite;
  pointer-events: none;
  z-index: 0;
}

@keyframes gridMove {
  0%   { background-position: 0 0, 0 0; }
  100% { background-position: 60px 60px, 60px 60px; }
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0.5rem !important; max-width: 1280px; position: relative; z-index: 1; }

/* ── Hero header ────────────────────────────── */
.zeus-hero {
  text-align: center;
  padding: 28px 0 12px;
  position: relative;
}

.zeus-logo {
  font-family: 'Bebas Neue', cursive;
  font-size: 5.5rem;
  line-height: 1;
  letter-spacing: 12px;
  background: linear-gradient(135deg, #39ff14 0%, #69ff47 40%, #ffb300 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: block;
  animation: logoGlow 4s ease-in-out infinite;
}

@keyframes logoGlow {
  0%,100% { filter: drop-shadow(0 0 8px rgba(57,255,20,0.4)); }
  50%      { filter: drop-shadow(0 0 24px rgba(57,255,20,0.8)); }
}

.zeus-tagline {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 0.85rem;
  letter-spacing: 5px;
  text-transform: uppercase;
  color: var(--muted);
  margin-top: 4px;
}

.zeus-bar {
  width: 80px;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--green), transparent);
  margin: 16px auto 0;
  animation: barPulse 2s ease-in-out infinite;
}

@keyframes barPulse {
  0%,100% { width: 80px; opacity: 0.6; }
  50%      { width: 180px; opacity: 1; }
}

/* ── Metrics row ────────────────────────────── */
.metrics-row {
  display: flex;
  gap: 12px;
  margin: 16px 0;
  flex-wrap: wrap;
}

.metric-box {
  flex: 1;
  min-width: 120px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px 16px;
  text-align: center;
  transition: border-color 0.3s;
}

.metric-box:hover { border-color: var(--green); }

.metric-val {
  font-family: 'Bebas Neue', cursive;
  font-size: 2.2rem;
  color: var(--green);
  line-height: 1;
  display: block;
}

.metric-val.gold { color: var(--gold); }

.metric-lbl {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 0.72rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

/* ── Scanning indicator ─────────────────────── */
.scan-line {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 0.8rem;
  color: var(--green);
  letter-spacing: 3px;
  text-transform: uppercase;
  text-align: center;
  padding: 8px;
  animation: scanFade 1s ease-in-out infinite;
}

@keyframes scanFade { 0%,100%{opacity:1;} 50%{opacity:0.25;} }

/* ── Pick cards ─────────────────────────────── */
.pick-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 22px 26px;
  margin: 14px 0;
  position: relative;
  overflow: hidden;
  opacity: 0;
  animation: cardReveal 0.5s ease forwards;
  transition: transform 0.25s, box-shadow 0.25s;
}

.pick-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(57,255,20,0.12);
}

/* Stagger animation delays */
.pick-card:nth-child(1) { animation-delay: 0.05s; }
.pick-card:nth-child(2) { animation-delay: 0.15s; }
.pick-card:nth-child(3) { animation-delay: 0.25s; }
.pick-card:nth-child(4) { animation-delay: 0.35s; }
.pick-card:nth-child(5) { animation-delay: 0.45s; }

@keyframes cardReveal {
  from { opacity:0; transform: translateY(16px); }
  to   { opacity:1; transform: translateY(0); }
}

.pick-card.elite {
  border-color: var(--gold);
  background: linear-gradient(135deg, #0f1e0f 0%, #1a1500 100%);
  animation: cardReveal 0.5s ease forwards, eliteGlow 3s ease-in-out infinite;
}

@keyframes eliteGlow {
  0%,100% { box-shadow: 0 0 16px rgba(255,179,0,0.1); }
  50%      { box-shadow: 0 0 40px rgba(255,179,0,0.3), 0 0 80px rgba(255,179,0,0.08); }
}

.pick-card.strong {
  border-color: var(--green2);
}

/* Rank badge */
.rank-badge {
  position: absolute;
  top: 14px;
  right: 20px;
  font-family: 'Bebas Neue', cursive;
  font-size: 4rem;
  line-height: 1;
  color: rgba(57,255,20,0.06);
  pointer-events: none;
  user-select: none;
}

.rank-badge.elite-rank { color: rgba(255,179,0,0.08); }

/* Card content */
.card-league {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 0.72rem;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 6px;
}

.card-teams {
  font-family: 'Bebas Neue', cursive;
  font-size: 2rem;
  letter-spacing: 3px;
  color: var(--text);
  line-height: 1.1;
  margin-bottom: 10px;
}

.card-vs {
  color: var(--muted);
  font-size: 1rem;
  padding: 0 8px;
}

.card-bet {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 1.5rem;
  letter-spacing: 1px;
  margin-bottom: 12px;
}

.card-bet.elite { color: var(--gold); }
.card-bet.strong { color: var(--green); }
.card-bet.good { color: #69ff47; }

/* Confidence bar */
.conf-track {
  background: rgba(255,255,255,0.06);
  border-radius: 999px;
  height: 6px;
  margin: 8px 0 10px;
  overflow: hidden;
}

.conf-fill {
  height: 100%;
  border-radius: 999px;
  animation: fillBar 1.2s cubic-bezier(0.22,1,0.36,1) forwards;
  transform-origin: left;
}

.conf-fill.elite { background: linear-gradient(90deg, var(--gold2), var(--gold)); }
.conf-fill.strong { background: linear-gradient(90deg, var(--green2), var(--green)); }
.conf-fill.good   { background: linear-gradient(90deg, #00b341, #39ff14); }

@keyframes fillBar { from { width: 0 !important; } }

.conf-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.conf-pct {
  font-family: 'Bebas Neue', cursive;
  font-size: 1.6rem;
  letter-spacing: 2px;
}

.conf-pct.elite  { color: var(--gold); }
.conf-pct.strong { color: var(--green); }
.conf-pct.good   { color: #69ff47; }

.tier-chip {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  padding: 3px 10px;
  border-radius: 999px;
}

.tier-chip.elite  { background: rgba(255,179,0,0.15); color: var(--gold); border: 1px solid rgba(255,179,0,0.4); }
.tier-chip.strong { background: rgba(57,255,20,0.1);  color: var(--green); border: 1px solid rgba(57,255,20,0.3); }
.tier-chip.good   { background: rgba(105,255,71,0.08); color: #69ff47; border: 1px solid rgba(105,255,71,0.25); }

/* Pills row */
.pills-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 10px;
}

.pill {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 0.75rem;
  letter-spacing: 1px;
  padding: 3px 10px;
  border-radius: 6px;
  white-space: nowrap;
}

.pill-time  { background: rgba(57,255,20,0.08); color: var(--green); border: 1px solid rgba(57,255,20,0.2); }
.pill-xg    { background: rgba(255,179,0,0.08); color: var(--gold); border: 1px solid rgba(255,179,0,0.2); }
.pill-over  { background: rgba(0,200,83,0.08); color: #00c853; border: 1px solid rgba(0,200,83,0.2); }
.pill-btts  { background: rgba(41,182,246,0.08); color: #29b6f6; border: 1px solid rgba(41,182,246,0.2); }
.pill-games { background: rgba(255,255,255,0.04); color: var(--muted); border: 1px solid rgba(255,255,255,0.08); }

/* Reasoning */
.card-reason {
  font-family: 'Barlow', sans-serif;
  font-size: 0.82rem;
  color: var(--muted);
  margin-top: 10px;
  line-height: 1.5;
  border-left: 2px solid var(--border);
  padding-left: 10px;
}

/* Countdown */
.countdown {
  font-family: 'Bebas Neue', cursive;
  font-size: 0.95rem;
  letter-spacing: 3px;
}

/* History table */
.result-won  { color: #39ff14; font-weight: 700; }
.result-lost { color: #ff1744; font-weight: 700; }
.result-pend { color: #ffb300; }

/* Tab bar overrides */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface);
  border-radius: 12px;
  padding: 4px;
  gap: 2px;
  border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
  border-radius: 8px;
  font-family: 'Barlow Condensed', sans-serif;
  letter-spacing: 1px;
  color: var(--muted);
  font-size: 0.9rem;
}
.stTabs [aria-selected="true"] {
  background: rgba(57,255,20,0.12) !important;
  color: var(--green) !important;
}

/* No-picks message */
.no-picks {
  text-align: center;
  padding: 48px 24px;
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 1.1rem;
  color: var(--muted);
  letter-spacing: 2px;
}

.no-picks-icon { font-size: 3rem; display: block; margin-bottom: 12px; }

/* Dividers */
hr { border-color: rgba(57,255,20,0.08) !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════

ESPN_SOCCER = "https://site.api.espn.com/apis/site/v2/sports/soccer"

CAT_OFFSET = timedelta(hours=2)   # Central Africa Time = UTC+2
WINDOW_HOURS = 4                   # only games kicking off within this many hours
MIN_GAMES_FOR_STATS = 5            # minimum completed games to produce a pick
OVER_LINE = 2.5                    # standard OVER line
TOP_N = 5                          # return only top N picks

# Confidence tier thresholds
TIER_ELITE  = 72   # 🔥 ELITE
TIER_STRONG = 60   # ⚡ STRONG
# below TIER_STRONG = ✅ CONFIDENT (still shows)

# All leagues to scan — ESPN soccer league IDs
LEAGUES: List[Tuple[str, str, str]] = [
    ("eng.1",               "Premier League",          "🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
    ("eng.2",               "Championship",            "🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
    ("esp.1",               "La Liga",                 "🇪🇸"),
    ("esp.2",               "Segunda División",        "🇪🇸"),
    ("ger.1",               "Bundesliga",              "🇩🇪"),
    ("ger.2",               "2. Bundesliga",           "🇩🇪"),
    ("ita.1",               "Serie A",                 "🇮🇹"),
    ("ita.2",               "Serie B",                 "🇮🇹"),
    ("fra.1",               "Ligue 1",                 "🇫🇷"),
    ("fra.2",               "Ligue 2",                 "🇫🇷"),
    ("ned.1",               "Eredivisie",              "🇳🇱"),
    ("por.1",               "Primeira Liga",           "🇵🇹"),
    ("sco.1",               "Scottish Premiership",    "🏴󠁧󠁢󠁳󠁣󠁴󠁿"),
    ("tur.1",               "Süper Lig",               "🇹🇷"),
    ("bel.1",               "Belgian Pro League",      "🇧🇪"),
    ("gre.1",               "Super League Greece",     "🇬🇷"),
    ("rus.1",               "Russian Premier",         "🇷🇺"),
    ("ukr.1",               "Ukrainian Premier",       "🇺🇦"),
    ("usa.1",               "MLS",                     "🇺🇸"),
    ("mex.1",               "Liga MX",                 "🇲🇽"),
    ("bra.1",               "Brasileirão",             "🇧🇷"),
    ("arg.1",               "Primera División",        "🇦🇷"),
    ("col.1",               "Liga Betplay",            "🇨🇴"),
    ("chi.1",               "Primera Chile",           "🇨🇱"),
    ("jpn.1",               "J1 League",               "🇯🇵"),
    ("kor.1",               "K League 1",              "🇰🇷"),
    ("chn.1",               "Chinese Super League",    "🇨🇳"),
    ("aus.1",               "A-League",                "🇦🇺"),
    ("sau.1",               "Saudi Pro League",        "🇸🇦"),
    ("egy.1",               "Egyptian Premier",        "🇪🇬"),
    ("rsa.1",               "PSL South Africa",        "🇿🇦"),
    ("ned.2",               "Eerste Divisie",          "🇳🇱"),
    ("uefa.champions",      "Champions League",        "🏆"),
    ("uefa.europa",         "Europa League",           "🟠"),
    ("uefa.europaconference","Conference League",      "🟢"),
    ("conmebol.libertadores","Copa Libertadores",      "🏆"),
]

STATUS_FINAL = {"STATUS_FINAL", "Final", "FT", "full-time"}

# ══════════════════════════════════════════════════════════════
#  DATABASE / CACHE
# ══════════════════════════════════════════════════════════════

@st.cache_resource
def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect("zeus_football.db", check_same_thread=False)
    conn.execute("""CREATE TABLE IF NOT EXISTS api_cache (
        cache_key TEXT PRIMARY KEY,
        data      TEXT,
        ts        REAL
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS picks_log (
        id         TEXT PRIMARY KEY,
        match      TEXT,
        league     TEXT,
        bet        TEXT,
        xg_total   REAL,
        confidence REAL,
        kickoff    TEXT,
        result     TEXT DEFAULT 'pending',
        logged_at  TEXT
    )""")
    conn.commit()
    return conn


def cache_get(key: str, ttl: int) -> Optional[Any]:
    try:
        conn = get_db()
        row = conn.execute(
            "SELECT data, ts FROM api_cache WHERE cache_key=?", (key,)
        ).fetchone()
        if row and (time.time() - row[1]) < ttl:
            return json.loads(row[0])
    except Exception:
        pass
    return None


def cache_set(key: str, data: Any):
    try:
        conn = get_db()
        conn.execute(
            "INSERT OR REPLACE INTO api_cache VALUES (?,?,?)",
            (key, json.dumps(data, default=str), time.time())
        )
        conn.commit()
    except Exception:
        pass


def save_pick(pick: Dict):
    try:
        pid = hashlib.md5(f"{pick['match']}{pick['kickoff']}".encode()).hexdigest()[:12]
        conn = get_db()
        conn.execute("""INSERT OR IGNORE INTO picks_log
            (id, match, league, bet, xg_total, confidence, kickoff, logged_at)
            VALUES (?,?,?,?,?,?,?,?)""", (
            pid, pick["match"], pick["league"], pick["bet"],
            pick["xg_total"], pick["confidence"], pick["kickoff"],
            datetime.utcnow().isoformat()
        ))
        conn.commit()
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════
#  API HELPERS
# ══════════════════════════════════════════════════════════════

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
}


def safe_get(url: str, params: Dict = None, timeout: int = 10) -> Optional[Dict]:
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def to_cat(utc_str: str) -> str:
    """ESPN UTC string → CAT display."""
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        cat = dt + CAT_OFFSET
        return cat.strftime("%d %b · %H:%M CAT")
    except Exception:
        return "—"


def parse_utc(utc_str: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
    except Exception:
        return None


def in_window(utc_str: str) -> bool:
    """True if kickoff is within the next WINDOW_HOURS hours."""
    dt = parse_utc(utc_str)
    if not dt:
        return False
    now = datetime.now(timezone.utc)
    return now <= dt <= now + timedelta(hours=WINDOW_HOURS)


def minutes_to_kickoff(utc_str: str) -> int:
    dt = parse_utc(utc_str)
    if not dt:
        return 9999
    now = datetime.now(timezone.utc)
    return max(0, int((dt - now).total_seconds() / 60))


# ══════════════════════════════════════════════════════════════
#  ESPN FETCHERS
# ══════════════════════════════════════════════════════════════

def fetch_scoreboard(league_id: str) -> List[Dict]:
    """Today's + tomorrow's fixtures for a league."""
    result = []
    for delta in [0, 1]:
        date_str = (datetime.utcnow() + timedelta(days=delta)).strftime("%Y%m%d")
        key = f"sb_{league_id}_{date_str}"
        cached = cache_get(key, ttl=300)
        if cached is not None:
            result.extend(cached)
            continue
        data = safe_get(f"{ESPN_SOCCER}/{league_id}/scoreboard", params={"dates": date_str})
        if not data:
            continue
        events = []
        for ev in data.get("events", []):
            comps = ev.get("competitions", [])
            if not comps:
                continue
            comp = comps[0]
            competitors = comp.get("competitors", [])
            if len(competitors) < 2:
                continue
            home_c = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
            away_c = next((c for c in competitors if c.get("homeAway") == "away"), competitors[1])
            status_type = comp.get("status", {}).get("type", {})
            events.append({
                "event_id":   ev.get("id", ""),
                "date":       ev.get("date", ""),
                "home_id":    str(home_c.get("team", {}).get("id", "")),
                "home_name":  home_c.get("team", {}).get("displayName", ""),
                "away_id":    str(away_c.get("team", {}).get("id", "")),
                "away_name":  away_c.get("team", {}).get("displayName", ""),
                "status":     status_type.get("name", ""),
                "completed":  status_type.get("completed", False),
                "league_id":  league_id,
            })
        cache_set(key, events)
        result.extend(events)
    return result


def fetch_team_schedule(league_id: str, team_id: str) -> List[Dict]:
    """Last 25 completed games for a team."""
    key = f"sched_{league_id}_{team_id}_{datetime.utcnow().strftime('%Y%m%d')}"
    cached = cache_get(key, ttl=3600)
    if cached is not None:
        return cached

    data = safe_get(f"{ESPN_SOCCER}/{league_id}/teams/{team_id}/schedule")
    if not data:
        return []

    games = []
    for ev in data.get("events", []):
        comps = ev.get("competitions", [])
        if not comps:
            continue
        comp = comps[0]
        competitors = comp.get("competitors", [])
        if len(competitors) < 2:
            continue
        status_t = comp.get("status", {}).get("type", {})
        if not status_t.get("completed", False):
            continue

        home_c = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
        away_c = next((c for c in competitors if c.get("homeAway") == "away"), competitors[1])

        def _score(raw) -> int:
            if raw is None:
                return 0
            if isinstance(raw, dict):
                raw = raw.get("value", raw.get("displayValue", 0))
            try:
                return int(float(str(raw)))
            except (ValueError, TypeError):
                return 0

        hs = _score(home_c.get("score"))
        as_ = _score(away_c.get("score"))

        games.append({
            "date":       ev.get("date", ""),
            "home_name":  home_c.get("team", {}).get("displayName", ""),
            "away_name":  away_c.get("team", {}).get("displayName", ""),
            "home_score": hs,
            "away_score": as_,
            "total":      hs + as_,
        })

    # Sort chronological, keep last 25 completed
    games.sort(key=lambda g: g["date"])
    games = games[-25:]
    cache_set(key, games)
    return games


# ══════════════════════════════════════════════════════════════
#  STATISTICS ENGINE
# ══════════════════════════════════════════════════════════════

def team_stats(games: List[Dict], team_name: str) -> Optional[Dict]:
    """
    Compute key stats from completed game log.
    Returns dict with scoring averages, over rates, BTTS rate.
    Returns None if insufficient data.
    """
    completed = [g for g in games if g.get("total", 0) > 0 or
                 g.get("home_score", 0) > 0 or g.get("away_score", 0) > 0]

    if len(completed) < MIN_GAMES_FOR_STATS:
        return None

    scored, conceded, totals = [], [], []
    for g in completed:
        is_home = g.get("home_name", "") == team_name
        sc = g["home_score"] if is_home else g["away_score"]
        co = g["away_score"] if is_home else g["home_score"]
        scored.append(sc)
        conceded.append(co)
        totals.append(sc + co)

    n = len(scored)
    avg_scored    = float(np.mean(scored))
    avg_conceded  = float(np.mean(conceded))
    avg_total     = float(np.mean(totals))
    over25_rate   = sum(1 for t in totals if t > 2.5) / n
    btts_rate     = sum(1 for i in range(n) if scored[i] > 0 and conceded[i] > 0) / n

    # Recent form (last 5 vs older) — are games getting higher-scoring?
    recent_avg  = float(np.mean(totals[-5:])) if n >= 5 else avg_total
    older_avg   = float(np.mean(totals[:-5])) if n > 5 else avg_total
    trend_score = max(0.0, min(1.0, 0.5 + (recent_avg - older_avg) / 4))

    return {
        "n":             n,
        "avg_scored":    avg_scored,
        "avg_conceded":  avg_conceded,
        "avg_total":     avg_total,
        "over25_rate":   over25_rate,
        "btts_rate":     btts_rate,
        "trend_score":   trend_score,
        "recent_avg":    recent_avg,
    }


def compute_confidence(home_st: Dict, away_st: Dict) -> Tuple[float, float, str]:
    """
    Returns (confidence %, xG total, reasoning string).

    Model:
      xG_home = 0.55 * home_avg_scored + 0.45 * away_avg_conceded
      xG_away = 0.55 * away_avg_scored + 0.45 * home_avg_conceded
      total_xG = xG_home + xG_away

    Confidence components:
      (A) xG component (45%) — how far above 2.5 line
      (B) Historical OVER 2.5 rate (40%) — both teams combined
      (C) BTTS rate (10%) — proxy for open attacking play
      (D) Trend (5%)  — recent games getting higher scoring
    """
    xg_home = 0.55 * home_st["avg_scored"] + 0.45 * away_st["avg_conceded"]
    xg_away = 0.55 * away_st["avg_scored"] + 0.45 * home_st["avg_conceded"]
    total_xg = xg_home + xg_away

    # xG score: 1.0→0%, 4.5→100%
    xg_score = max(0.0, min(100.0, (total_xg - 1.0) / 3.5 * 100.0))

    # Over rate score (0–100)
    combined_over = (home_st["over25_rate"] + away_st["over25_rate"]) / 2
    over_score = combined_over * 100.0

    # BTTS score
    combined_btts = (home_st["btts_rate"] + away_st["btts_rate"]) / 2
    btts_score = combined_btts * 100.0

    # Trend score
    trend = (home_st["trend_score"] + away_st["trend_score"]) / 2
    trend_score = trend * 100.0

    confidence = (
        xg_score   * 0.45 +
        over_score * 0.40 +
        btts_score * 0.10 +
        trend_score * 0.05
    )

    reasons = []
    reasons.append(f"xG model: {total_xg:.2f} total expected goals")
    reasons.append(
        f"OVER 2.5 rate: {home_st['over25_rate']*100:.0f}% (home) / "
        f"{away_st['over25_rate']*100:.0f}% (away)"
    )
    reasons.append(f"BTTS: {combined_btts*100:.0f}% of combined games")
    if home_st["recent_avg"] > home_st["avg_total"] + 0.3:
        reasons.append("Home team's recent games trending higher-scoring ↑")
    if away_st["recent_avg"] > away_st["avg_total"] + 0.3:
        reasons.append("Away team's recent games trending higher-scoring ↑")

    return round(confidence, 1), round(total_xg, 2), " · ".join(reasons)


def get_tier(conf: float) -> str:
    if conf >= TIER_ELITE:  return "elite"
    if conf >= TIER_STRONG: return "strong"
    return "good"


def get_tier_label(conf: float) -> str:
    if conf >= TIER_ELITE:  return "🔥 ELITE"
    if conf >= TIER_STRONG: return "⚡ STRONG"
    return "✅ CONFIDENT"


# ══════════════════════════════════════════════════════════════
#  MAIN SCANNER — produces top 5 picks
# ══════════════════════════════════════════════════════════════

@st.cache_data(ttl=300, show_spinner=False)
def scan_all_leagues() -> Tuple[List[Dict], int, int]:
    """
    Scans all leagues for games in the next WINDOW_HOURS hours.
    Returns (top_5_picks, leagues_scanned, games_evaluated).
    """
    candidates: List[Dict] = []
    leagues_hit = 0
    games_eval  = 0

    for league_id, league_name, flag in LEAGUES:
        events = fetch_scoreboard(league_id)
        if not events:
            continue

        # Filter to upcoming games in window
        window_games = [e for e in events
                        if not e.get("completed", False) and in_window(e.get("date", ""))]
        if not window_games:
            continue

        leagues_hit += 1

        for ev in window_games:
            home_games = fetch_team_schedule(league_id, ev["home_id"])
            away_games = fetch_team_schedule(league_id, ev["away_id"])

            home_st = team_stats(home_games, ev["home_name"])
            away_st = team_stats(away_games, ev["away_name"])

            if home_st is None or away_st is None:
                continue

            games_eval += 1

            conf, xg_total, reasoning = compute_confidence(home_st, away_st)

            # Only candidates where xG > OVER_LINE (the model actually says OVER)
            if xg_total <= OVER_LINE:
                continue

            candidates.append({
                "rank":        0,   # set after sorting
                "match":       f"{ev['home_name']} vs {ev['away_name']}",
                "home":        ev["home_name"],
                "away":        ev["away_name"],
                "league":      f"{flag} {league_name}",
                "league_id":   league_id,
                "kickoff_utc": ev["date"],
                "kickoff_cat": to_cat(ev["date"]),
                "mins_away":   minutes_to_kickoff(ev["date"]),
                "bet":         f"OVER {OVER_LINE}",
                "xg_total":    xg_total,
                "confidence":  conf,
                "tier":        get_tier(conf),
                "tier_label":  get_tier_label(conf),
                "reasoning":   reasoning,
                "home_over":   round(home_st["over25_rate"] * 100, 0),
                "away_over":   round(away_st["over25_rate"] * 100, 0),
                "home_btts":   round(home_st["btts_rate"] * 100, 0),
                "away_btts":   round(away_st["btts_rate"] * 100, 0),
                "home_n":      home_st["n"],
                "away_n":      away_st["n"],
                "home_avg_g":  round(home_st["avg_scored"], 2),
                "away_avg_g":  round(away_st["avg_scored"], 2),
            })

    # Sort by confidence descending, take top 5
    candidates.sort(key=lambda x: x["confidence"], reverse=True)
    top5 = candidates[:TOP_N]
    for i, p in enumerate(top5, 1):
        p["rank"] = i
        save_pick(p)

    return top5, leagues_hit, games_eval


# ══════════════════════════════════════════════════════════════
#  COUNTDOWN COMPONENT  (JavaScript, ticks every second)
# ══════════════════════════════════════════════════════════════

def countdown_html(kickoff_utc: str, pick_id: str) -> str:
    return f"""
<div id="cd_{pick_id}" class="countdown" style="color:#39ff14;font-size:0.85rem;letter-spacing:2px;">
  ⏱ Calculating...
</div>
<script>
(function() {{
  var target = new Date("{kickoff_utc}");
  var el = document.getElementById("cd_{pick_id}");
  function tick() {{
    var now = new Date();
    var diff = target - now;
    if (diff <= 0) {{
      el.innerHTML = "🔴 LIVE NOW";
      el.style.color = "#ff1744";
      return;
    }}
    var h = Math.floor(diff / 3600000);
    var m = Math.floor((diff % 3600000) / 60000);
    var s = Math.floor((diff % 60000) / 1000);
    var parts = [];
    if (h > 0) parts.push(h + "h");
    parts.push(("0"+m).slice(-2) + "m");
    parts.push(("0"+s).slice(-2) + "s");
    el.innerHTML = "⏱ KICKOFF IN " + parts.join(" ");
  }}
  tick();
  setInterval(tick, 1000);
}})();
</script>
"""


# ══════════════════════════════════════════════════════════════
#  PICK CARD RENDERER
# ══════════════════════════════════════════════════════════════

def render_pick_card(pick: Dict):
    tier  = pick["tier"]
    conf  = pick["confidence"]
    elite = tier == "elite"

    card_cls = f"pick-card {tier}"
    rank_cls = f"rank-badge {'elite-rank' if elite else ''}"
    bet_cls  = f"card-bet {tier}"
    pct_cls  = f"conf-pct {tier}"
    chip_cls = f"tier-chip {tier}"
    bar_cls  = f"conf-fill {tier}"

    pick_id = hashlib.md5(pick["match"].encode()).hexdigest()[:6]
    bar_width = min(99, int(conf))

    card_html = f"""
<div class="{card_cls}">
  <div class="{rank_cls}">#{pick["rank"]}</div>

  <div class="card-league">{pick["league"]}</div>
  <div class="card-teams">{pick["home"]} <span class="card-vs">vs</span> {pick["away"]}</div>

  <div class="{bet_cls}">⚽ OVER {OVER_LINE} GOALS</div>

  <div class="conf-row">
    <span class="{pct_cls}">{conf:.1f}%</span>
    <span class="{chip_cls}">{pick["tier_label"]}</span>
  </div>
  <div class="conf-track">
    <div class="{bar_cls}" style="width:{bar_width}%;"></div>
  </div>

  <div class="pills-row">
    <span class="pill pill-time">{pick["kickoff_cat"]}</span>
    <span class="pill pill-xg">xG: {pick["xg_total"]:.2f}</span>
    <span class="pill pill-over">OVER%: {pick["home_over"]:.0f} / {pick["away_over"]:.0f}</span>
    <span class="pill pill-btts">BTTS%: {pick["home_btts"]:.0f} / {pick["away_btts"]:.0f}</span>
    <span class="pill pill-games">{pick["home_n"]}+{pick["away_n"]} games</span>
  </div>

  <div class="card-reason">
    {pick["reasoning"]}
  </div>
</div>
"""
    st.markdown(card_html, unsafe_allow_html=True)
    # Live countdown below card
    components.html(countdown_html(pick["kickoff_utc"], pick_id), height=28)


# ══════════════════════════════════════════════════════════════
#  RESULTS GRADER
# ══════════════════════════════════════════════════════════════

def grade_picks():
    """
    Attempt to grade pending picks by fetching their game result.
    A pick is graded WON if the match total > 2.5, LOST otherwise.
    """
    conn = get_db()
    pending = conn.execute(
        "SELECT id, match, league_id, kickoff FROM picks_log WHERE result='pending'"
    ).fetchall()
    updated = 0

    for row_id, match, league_id, kickoff in pending:
        # Only grade if kickoff was more than 100 minutes ago (match finished)
        ko = parse_utc(kickoff)
        if not ko:
            continue
        if (datetime.now(timezone.utc) - ko).total_seconds() < 6000:
            continue

        # Parse team names from "Home vs Away"
        parts = match.split(" vs ")
        if len(parts) != 2:
            continue
        home_name, away_name = parts[0].strip(), parts[1].strip()

        # Need league_id to fetch schedule — stored in DB, use league_id if available
        if not league_id:
            continue

        # Find both teams' IDs from a recent scoreboard (approximate — use date)
        date_str = ko.strftime("%Y%m%d")
        data = safe_get(
            f"{ESPN_SOCCER}/{league_id}/scoreboard",
            params={"dates": date_str}
        )
        if not data:
            continue

        for ev in data.get("events", []):
            comps = ev.get("competitions", [])
            if not comps:
                continue
            comp = comps[0]
            if not comp.get("status", {}).get("type", {}).get("completed", False):
                continue
            competitors = comp.get("competitors", [])
            if len(competitors) < 2:
                continue
            names = {c.get("team", {}).get("displayName", "") for c in competitors}
            if home_name not in names and away_name not in names:
                continue

            # Extract scores
            def _sc(raw):
                if isinstance(raw, dict):
                    raw = raw.get("value", raw.get("displayValue", 0))
                try: return int(float(str(raw)))
                except: return 0

            total = sum(_sc(c.get("score")) for c in competitors)
            result = "WON" if total > 2.5 else "LOST"
            conn.execute("UPDATE picks_log SET result=? WHERE id=?", (result, row_id))
            updated += 1
            break

    if updated:
        conn.commit()
    return updated


# ══════════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════════

def main():
    # Auto-refresh every 5 minutes
    try:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=300_000, key="zeus_refresh")
    except ImportError:
        pass

    # ── Hero ─────────────────────────────────────────────────
    st.markdown("""
<div class="zeus-hero">
  <span class="zeus-logo">⚽ ZEUS</span>
  <div class="zeus-tagline">Football Intelligence · OVER 2.5 Goals · Top 5 World Picks</div>
  <div class="zeus-bar"></div>
</div>
""", unsafe_allow_html=True)

    # ── Tabs ─────────────────────────────────────────────────
    tab_picks, tab_results, tab_leagues = st.tabs([
        "🎯 Top 5 Picks",
        "🏆 Results",
        "🌍 Leagues Scanned"
    ])

    # ══════════════════════════════════════════════════════════
    #  TAB 1 — TOP 5 PICKS
    # ══════════════════════════════════════════════════════════
    with tab_picks:
        now_cat = (datetime.utcnow() + CAT_OFFSET).strftime("%d %b %Y · %H:%M CAT")
        st.caption(f"🕐 {now_cat} &nbsp;·&nbsp; Scanning games kicking off in the next {WINDOW_HOURS} hours &nbsp;·&nbsp; Auto-refresh 5min")

        with st.spinner(""):
            st.markdown('<div class="scan-line">⚡ SCANNING GLOBAL LEAGUES ⚡</div>', unsafe_allow_html=True)
            picks, leagues_scanned, games_eval = scan_all_leagues()

        # ── Summary metrics ──────────────────────────────────
        elite_cnt  = sum(1 for p in picks if p["tier"] == "elite")
        strong_cnt = sum(1 for p in picks if p["tier"] == "strong")

        metrics_html = f"""
<div class="metrics-row">
  <div class="metric-box">
    <span class="metric-val">{len(picks)}</span>
    <div class="metric-lbl">Picks Today</div>
  </div>
  <div class="metric-box">
    <span class="metric-val gold">{elite_cnt}</span>
    <div class="metric-lbl">🔥 Elite</div>
  </div>
  <div class="metric-box">
    <span class="metric-val">{strong_cnt}</span>
    <div class="metric-lbl">⚡ Strong</div>
  </div>
  <div class="metric-box">
    <span class="metric-val">{leagues_scanned}</span>
    <div class="metric-lbl">Leagues Hit</div>
  </div>
  <div class="metric-box">
    <span class="metric-val">{games_eval}</span>
    <div class="metric-lbl">Games Evaluated</div>
  </div>
</div>
"""
        st.markdown(metrics_html, unsafe_allow_html=True)
        st.markdown("---")

        if not picks:
            st.markdown("""
<div class="no-picks">
  <span class="no-picks-icon">⏳</span>
  No games with sufficient statistical confidence in the next 4 hours.<br>
  Check back as more fixtures enter the window, or wait for league schedules to update.
</div>
""", unsafe_allow_html=True)
        else:
            # Confidence tier legend
            col_a, col_b, col_c = st.columns(3)
            col_a.markdown(
                '<span style="font-family:Barlow Condensed;color:#ffb300;font-size:0.85rem;">🔥 ELITE &nbsp;≥72% — '
                'Exceptional statistical edge, multiple strong signals</span>',
                unsafe_allow_html=True
            )
            col_b.markdown(
                '<span style="font-family:Barlow Condensed;color:#39ff14;font-size:0.85rem;">⚡ STRONG &nbsp;60–71% — '
                'Clear OVER signal, consistent historical data</span>',
                unsafe_allow_html=True
            )
            col_c.markdown(
                '<span style="font-family:Barlow Condensed;color:#69ff47;font-size:0.85rem;">✅ CONFIDENT &nbsp;<60% — '
                'Solid lean, less dominant but still positive xG</span>',
                unsafe_allow_html=True
            )
            st.markdown("---")

            for pick in picks:
                render_pick_card(pick)

    # ══════════════════════════════════════════════════════════
    #  TAB 2 — RESULTS
    # ══════════════════════════════════════════════════════════
    with tab_results:
        st.subheader("🏆 Pick Results — Correct vs Missed")

        with st.spinner("Grading picks…"):
            newly_graded = grade_picks()
        if newly_graded:
            st.toast(f"✅ Graded {newly_graded} new pick(s)!", icon="⚽")

        try:
            conn = get_db()
            rows = conn.execute("""
                SELECT match, league, bet, xg_total, confidence, kickoff, result, logged_at
                FROM picks_log ORDER BY logged_at DESC LIMIT 300
            """).fetchall()

            if not rows:
                st.info("No picks logged yet — go to 🎯 Top 5 Picks to generate predictions.")
            else:
                df = pd.DataFrame(rows, columns=[
                    "Match", "League", "Bet", "xG Total", "Confidence%", "Kickoff UTC", "Result", "Logged At"
                ])
                df["Confidence%"] = df["Confidence%"].apply(lambda x: f"{x:.1f}%")
                df["xG Total"]    = df["xG Total"].apply(lambda x: f"{x:.2f}")

                won  = df[df["Result"] == "WON"]
                lost = df[df["Result"] == "LOST"]
                pend = df[df["Result"] == "pending"]
                tot  = len(won) + len(lost)
                wr   = f"{len(won)/tot*100:.1f}%" if tot > 0 else "—"

                m1, m2, m3, m4, m5 = st.columns(5)
                m1.metric("✅ Won",    len(won))
                m2.metric("❌ Lost",   len(lost))
                m3.metric("⏳ Pending", len(pend))
                m4.metric("Total Graded", tot)
                m5.metric("Win Rate",  wr)

                st.divider()

                st.markdown("### ✅ Correct Picks")
                if won.empty:
                    st.info("No graded wins yet — picks are graded after matches complete (2h after kickoff).")
                else:
                    for _, r in won.iterrows():
                        st.markdown(
                            f"⚽ **{r['Match']}** &nbsp;·&nbsp; {r['League']} &nbsp;·&nbsp; "
                            f"**{r['Bet']}** &nbsp;·&nbsp; xG: {r['xG Total']} &nbsp;·&nbsp; "
                            f"Conf: **{r['Confidence%']}** &nbsp;·&nbsp; "
                            f"<span style='color:#39ff14;font-weight:700;'>WON ✅</span>",
                            unsafe_allow_html=True
                        )
                        st.divider()

                st.markdown("### ❌ Missed Picks")
                if lost.empty:
                    st.info("No missed picks graded yet.")
                else:
                    for _, r in lost.iterrows():
                        st.markdown(
                            f"⚽ **{r['Match']}** &nbsp;·&nbsp; {r['League']} &nbsp;·&nbsp; "
                            f"**{r['Bet']}** &nbsp;·&nbsp; xG: {r['xG Total']} &nbsp;·&nbsp; "
                            f"Conf: **{r['Confidence%']}** &nbsp;·&nbsp; "
                            f"<span style='color:#ff1744;font-weight:700;'>MISSED ❌</span>",
                            unsafe_allow_html=True
                        )
                        st.divider()

                if not pend.empty:
                    with st.expander(f"⏳ Pending — {len(pend)} picks awaiting results"):
                        st.dataframe(
                            pend[["Match", "League", "Bet", "Confidence%", "Kickoff UTC"]],
                            hide_index=True, use_container_width=True
                        )

        except Exception as e:
            st.info(f"Results log unavailable: {e}")

    # ══════════════════════════════════════════════════════════
    #  TAB 3 — LEAGUES SCANNED
    # ══════════════════════════════════════════════════════════
    with tab_leagues:
        st.subheader("🌍 All Leagues Monitored")
        st.caption(f"ZEUS scans {len(LEAGUES)} leagues globally every 5 minutes for games in the next {WINDOW_HOURS} hours.")
        st.markdown("")

        league_data = []
        for lid, lname, flag in LEAGUES:
            league_data.append({
                "Flag":   flag,
                "League": lname,
                "Region": lid.split(".")[0].upper(),
                "ESPN ID": lid,
            })

        df_leagues = pd.DataFrame(league_data)
        st.dataframe(df_leagues, hide_index=True, use_container_width=True)

        st.divider()
        st.caption(
            "**Data source:** ESPN Soccer API (free, no key required). "
            "Schedule data refreshes every hour. Scoreboard refreshes every 5 minutes. "
            "Picks are generated only for games with ≥5 completed games of historical data for both teams."
        )


if __name__ == "__main__":
    main()
