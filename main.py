import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import datetime
import time
from pathlib import Path
import yfinance as yf

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CAPITAL · Jean Pierre KARL",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get Help": None, "Report a bug": None, "About": "CAPITAL — Gestionnaire de Patrimoine v2.0"}
)

# ─── CSS PREMIUM ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Mono:wght@300;400;500&family=Syne:wght@400;500;600;700&display=swap');

:root {
  --bg: #07090d; --s1: #0d1018; --s2: #131820; --s3: #1a2030;
  --gold: #c9a84c; --gold2: #e8c97a; --gold3: #f5e4b0;
  --green: #27c994; --red: #e85252; --blue: #4a9cff; --purple: #9270ff;
  --text: #e4e8f0; --muted: #5a6880; --dim: #2a3448;
}

html, body, [class*="css"] {
  font-family: 'Syne', sans-serif !important;
  background-color: var(--bg) !important;
  color: var(--text) !important;
}

/* === HIDE STREAMLIT CHROME === */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
div[data-testid="stToolbar"] { display: none; }

/* === MAIN BG === */
.stApp { background: #07090d !important; }
section[data-testid="stSidebar"] {
  background: #0d1018 !important;
  border-right: 1px solid rgba(255,255,255,0.06) !important;
}

/* === SIDEBAR CONTENT === */
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stRadio label {
  color: #e4e8f0 !important;
  font-family: 'Syne', sans-serif !important;
}

section[data-testid="stSidebar"] .stRadio > div {
  gap: 4px;
}
section[data-testid="stSidebar"] .stRadio > div > label {
  background: #131820;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 10px;
  padding: 8px 12px;
  color: #5a6880 !important;
  font-size: 12px;
  transition: all .2s;
  cursor: pointer;
}
section[data-testid="stSidebar"] .stRadio > div > label:hover {
  border-color: #c9a84c;
  color: #e8c97a !important;
}
section[data-testid="stSidebar"] .stRadio > div > label[data-baseweb="radio"] {
  background: rgba(201,168,76,0.12);
  border-color: #c9a84c;
  color: #e8c97a !important;
}

/* === BUTTONS === */
.stButton > button {
  font-family: 'Syne', sans-serif !important;
  font-weight: 600 !important;
  border-radius: 10px !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  background: rgba(201,168,76,0.08) !important;
  color: #e8c97a !important;
  transition: all .2s !important;
}
.stButton > button:hover {
  background: rgba(201,168,76,0.18) !important;
  border-color: #c9a84c !important;
  transform: translateY(-1px);
}
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #c9a84c, #e8c97a) !important;
  color: #07090d !important;
  border: none !important;
  font-weight: 700 !important;
}

/* === INPUTS === */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > textarea {
  background: #131820 !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 10px !important;
  color: #e4e8f0 !important;
  font-family: 'Syne', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > textarea:focus {
  border-color: #c9a84c !important;
  box-shadow: 0 0 0 1px rgba(201,168,76,0.3) !important;
}
.stSelectbox > div > div > div { color: #e4e8f0 !important; }

/* === METRICS === */
[data-testid="metric-container"] {
  background: #0d1018 !important;
  border: 1px solid rgba(255,255,255,0.06) !important;
  border-radius: 16px !important;
  padding: 16px !important;
  transition: border-color .2s !important;
}
[data-testid="metric-container"]:hover {
  border-color: rgba(201,168,76,0.25) !important;
}
[data-testid="metric-container"] label {
  font-size: 9px !important;
  letter-spacing: 0.18em !important;
  text-transform: uppercase !important;
  color: #5a6880 !important;
  font-family: 'Syne', sans-serif !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 28px !important;
  font-weight: 700 !important;
  color: #e8c97a !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
  font-family: 'DM Mono', monospace !important;
  font-size: 12px !important;
}

/* === DATAFRAME === */
.stDataFrame {
  border: 1px solid rgba(255,255,255,0.06) !important;
  border-radius: 12px !important;
  overflow: hidden !important;
}
.stDataFrame table { background: #0d1018 !important; }
.stDataFrame thead tr th {
  background: #131820 !important;
  color: #5a6880 !important;
  font-family: 'Syne', sans-serif !important;
  font-size: 10px !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  border-bottom: 1px solid rgba(255,255,255,0.06) !important;
}
.stDataFrame tbody tr td {
  color: #e4e8f0 !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 12px !important;
  border-bottom: 1px solid rgba(255,255,255,0.03) !important;
}
.stDataFrame tbody tr:hover td { background: rgba(255,255,255,0.02) !important; }

/* === TABS === */
.stTabs [data-baseweb="tab-list"] {
  gap: 4px;
  background: #0d1018;
  padding: 6px;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,0.06);
}
.stTabs [data-baseweb="tab"] {
  border-radius: 10px;
  padding: 8px 18px;
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-weight: 600;
  color: #5a6880;
  background: transparent;
  border: none;
  font-family: 'Syne', sans-serif !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, #c9a84c, #e8c97a) !important;
  color: #07090d !important;
}

/* === ALERTS === */
.stAlert {
  border-radius: 12px !important;
  border: 1px solid !important;
}
div[data-baseweb="notification"][kind="error"],
.stAlert[data-baseweb="notification"] {
  background: rgba(232,82,82,0.08) !important;
  border-color: rgba(232,82,82,0.3) !important;
}
.element-container .stSuccess {
  background: rgba(39,201,148,0.08) !important;
  border-color: rgba(39,201,148,0.3) !important;
}
.element-container .stWarning {
  background: rgba(245,158,11,0.08) !important;
  border-color: rgba(245,158,11,0.3) !important;
}

/* === EXPANDER === */
.streamlit-expanderHeader {
  background: #0d1018 !important;
  border: 1px solid rgba(255,255,255,0.06) !important;
  border-radius: 12px !important;
  color: #e4e8f0 !important;
  font-family: 'Syne', sans-serif !important;
}
.streamlit-expanderContent {
  background: #0d1018 !important;
  border: 1px solid rgba(255,255,255,0.06) !important;
  border-top: none !important;
  border-radius: 0 0 12px 12px !important;
}

/* === SLIDER === */
.stSlider [data-baseweb="slider"] { padding: 4px 0; }
.stSlider [data-baseweb="thumb"] { background: #c9a84c !important; border-color: #c9a84c !important; }
.stSlider [data-baseweb="track-fill"] { background: linear-gradient(90deg, #c9a84c, #e8c97a) !important; }

/* === CUSTOM CARDS === */
.capital-card {
  background: #0d1018;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 18px;
  padding: 20px;
  margin-bottom: 14px;
  transition: border-color .2s;
}
.capital-card:hover { border-color: rgba(201,168,76,0.2); }
.capital-header {
  font-family: 'Cormorant Garamond', serif;
  font-size: 28px;
  font-weight: 700;
  color: #e8c97a;
  letter-spacing: 0.06em;
  margin: 0;
}
.capital-sub {
  font-size: 9px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: #5a6880;
  margin-top: 2px;
}
.kpi-label {
  font-size: 9px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #5a6880;
  font-family: 'Syne', sans-serif;
}
.kpi-value {
  font-family: 'Cormorant Garamond', serif;
  font-size: 26px;
  font-weight: 700;
}
.badge-green { color: #27c994; font-family: 'DM Mono', monospace; font-size: 12px; }
.badge-red { color: #e85252; font-family: 'DM Mono', monospace; font-size: 12px; }
.badge-gold { color: #e8c97a; font-family: 'DM Mono', monospace; font-size: 12px; }
.alert-box {
  background: rgba(232,82,82,0.08);
  border: 1px solid rgba(232,82,82,0.3);
  border-radius: 12px;
  padding: 14px 18px;
  margin-bottom: 10px;
  font-size: 13px;
}
.alert-box-warn {
  background: rgba(245,158,11,0.08);
  border: 1px solid rgba(245,158,11,0.3);
  border-radius: 12px;
  padding: 14px 18px;
  margin-bottom: 10px;
  font-size: 13px;
}
.ticker-scroll {
  background: rgba(201,168,76,0.05);
  border-top: 1px solid rgba(201,168,76,0.12);
  border-bottom: 1px solid rgba(201,168,76,0.12);
  padding: 10px 0;
  overflow: hidden;
  white-space: nowrap;
  font-family: 'DM Mono', monospace;
  font-size: 12px;
}
.section-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 22px;
  font-weight: 700;
  color: #f5e4b0;
  margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

# ─── DATA STORAGE (JSON FILES) ────────────────────────────────────────────────
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

ACCOUNTS_FILE  = DATA_DIR / "accounts.json"
INVESTMENTS_FILE = DATA_DIR / "investments.json"
EXPENSES_FILE  = DATA_DIR / "expenses.json"
BUDGETS_FILE   = DATA_DIR / "budgets.json"
GOALS_FILE     = DATA_DIR / "goals.json"
PROFILE_FILE   = DATA_DIR / "profile.json"

def load_json(path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except:
            return default
    return default

def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# ─── EURONEXT ACTIFS (from file 1 — NEXUS INVEST) ────────────────────────────
EURONEXT_ASSETS = [
    {"name":"EQUINOR","symbol":"EQNR.OL","market":"Oslo Børs","currency":"NOK","sector":"Energy","last":278.65,"change_pct":0.0},
    {"name":"ASML HOLDING","symbol":"ASML","market":"Euronext Amsterdam","currency":"EUR","sector":"Technology","last":606.0,"change_pct":0.0},
    {"name":"DNB BANK","symbol":"DNB.OL","market":"Oslo Børs","currency":"NOK","sector":"Finance","last":275.5,"change_pct":0.0},
    {"name":"UNICREDIT","symbol":"UCG.MI","market":"Euronext Milan","currency":"EUR","sector":"Finance","last":51.53,"change_pct":0.0},
    {"name":"INTESA SANPAOLO","symbol":"ISP.MI","market":"Euronext Milan","currency":"EUR","sector":"Finance","last":4.734,"change_pct":0.0},
    {"name":"LVMH","symbol":"MC.PA","market":"Euronext Paris","currency":"EUR","sector":"Luxury","last":571.7,"change_pct":0.0},
    {"name":"KONGSBERG GRUPPEN","symbol":"KOG.OL","market":"Oslo Børs","currency":"NOK","sector":"Defense","last":1535.0,"change_pct":0.0},
    {"name":"BNP PARIBAS","symbol":"BNP.PA","market":"Euronext Paris","currency":"EUR","sector":"Finance","last":76.91,"change_pct":0.0},
    {"name":"AKER BP","symbol":"AKRBP.OL","market":"Oslo Børs","currency":"NOK","sector":"Energy","last":249.5,"change_pct":0.0},
    {"name":"ENEL","symbol":"ENEL.MI","market":"Euronext Milan","currency":"EUR","sector":"Utilities","last":7.497,"change_pct":0.0},
    {"name":"TOTALENERGIES","symbol":"TTE.PA","market":"Euronext Paris","currency":"EUR","sector":"Energy","last":56.2,"change_pct":0.0},
    {"name":"STELLANTIS","symbol":"STLAM.MI","market":"Euronext Milan","currency":"EUR","sector":"Automotive","last":10.05,"change_pct":0.0},
    {"name":"AIRBUS","symbol":"AIR.PA","market":"Euronext Paris","currency":"EUR","sector":"Aerospace","last":162.76,"change_pct":0.0},
    {"name":"SANOFI","symbol":"SAN.PA","market":"Euronext Paris","currency":"EUR","sector":"Healthcare","last":95.62,"change_pct":0.0},
    {"name":"KERING","symbol":"KER.PA","market":"Euronext Paris","currency":"EUR","sector":"Luxury","last":171.5,"change_pct":0.0},
    {"name":"AXA","symbol":"CS.PA","market":"Euronext Paris","currency":"EUR","sector":"Insurance","last":36.96,"change_pct":0.0},
    {"name":"LOREAL","symbol":"OR.PA","market":"Euronext Paris","currency":"EUR","sector":"Consumer","last":283.5,"change_pct":0.0},
    {"name":"SAFRAN","symbol":"SAF.PA","market":"Euronext Paris","currency":"EUR","sector":"Aerospace","last":268.8,"change_pct":0.0},
    {"name":"CREDIT AGRICOLE","symbol":"ACA.PA","market":"Euronext Paris","currency":"EUR","sector":"Finance","last":17.57,"change_pct":0.0},
    {"name":"SCHNEIDER ELECTRIC","symbol":"SU.PA","market":"Euronext Paris","currency":"EUR","sector":"Technology","last":207.9,"change_pct":0.0},
    {"name":"STMICROELECTRONICS","symbol":"STM.PA","market":"Euronext Paris","currency":"EUR","sector":"Technology","last":21.27,"change_pct":0.0},
    {"name":"HERMES INTL","symbol":"RMS.PA","market":"Euronext Paris","currency":"EUR","sector":"Luxury","last":2415.0,"change_pct":0.0},
    {"name":"SOCIETE GENERALE","symbol":"GLE.PA","market":"Euronext Paris","currency":"EUR","sector":"Finance","last":37.78,"change_pct":0.0},
    {"name":"VINCI","symbol":"DG.PA","market":"Euronext Paris","currency":"EUR","sector":"Construction","last":101.4,"change_pct":0.0},
    {"name":"FERRARI","symbol":"RACE.MI","market":"Euronext Milan","currency":"EUR","sector":"Automotive","last":393.6,"change_pct":0.0},
    {"name":"CAPGEMINI","symbol":"CAP.PA","market":"Euronext Paris","currency":"EUR","sector":"Technology","last":154.3,"change_pct":0.0},
    {"name":"DASSAULT SYSTEMES","symbol":"DSY.PA","market":"Euronext Paris","currency":"EUR","sector":"Technology","last":24.92,"change_pct":0.0},
    {"name":"PUBLICIS GROUPE","symbol":"PUB.PA","market":"Euronext Paris","currency":"EUR","sector":"Media","last":100.3,"change_pct":0.0},
    {"name":"DANONE","symbol":"BN.PA","market":"Euronext Paris","currency":"EUR","sector":"Consumer","last":65.1,"change_pct":0.0},
    {"name":"ORANGE","symbol":"ORA.PA","market":"Euronext Paris","currency":"EUR","sector":"Telecom","last":10.42,"change_pct":0.0},
    {"name":"SAINT GOBAIN","symbol":"SGO.PA","market":"Euronext Paris","currency":"EUR","sector":"Materials","last":75.3,"change_pct":0.0},
    {"name":"ENI","symbol":"ENI.MI","market":"Euronext Milan","currency":"EUR","sector":"Energy","last":13.27,"change_pct":0.0},
    {"name":"RENAULT","symbol":"RNO.PA","market":"Euronext Paris","currency":"EUR","sector":"Automotive","last":48.3,"change_pct":0.0},
    {"name":"MEDIOBANCA","symbol":"MB.MI","market":"Euronext Milan","currency":"EUR","sector":"Finance","last":16.615,"change_pct":0.0},
    {"name":"MONCLER","symbol":"MONC.MI","market":"Euronext Milan","currency":"EUR","sector":"Luxury","last":46.03,"change_pct":0.0},
    {"name":"SCOR SE","symbol":"SCR.PA","market":"Euronext Paris","currency":"EUR","sector":"Insurance","last":26.14,"change_pct":0.0},
    {"name":"ALSTOM","symbol":"ALO.PA","market":"Euronext Paris","currency":"EUR","sector":"Transportation","last":16.4,"change_pct":0.0},
    {"name":"MICHELIN","symbol":"ML.PA","market":"Euronext Paris","currency":"EUR","sector":"Automotive","last":33.85,"change_pct":0.0},
    {"name":"LEGRAND","symbol":"LR.PA","market":"Euronext Paris","currency":"EUR","sector":"Technology","last":89.7,"change_pct":0.0},
    {"name":"PERNOD RICARD","symbol":"RI.PA","market":"Euronext Paris","currency":"EUR","sector":"Consumer","last":77.9,"change_pct":0.0},
]

# Additional popular tickers for portfolio
EXTRA_TICKERS = [
    {"name":"APPLE","symbol":"AAPL","market":"NASDAQ","currency":"USD","sector":"Technology","last":0},
    {"name":"MICROSOFT","symbol":"MSFT","market":"NASDAQ","currency":"USD","sector":"Technology","last":0},
    {"name":"NVIDIA","symbol":"NVDA","market":"NASDAQ","currency":"USD","sector":"Technology","last":0},
    {"name":"TESLA","symbol":"TSLA","market":"NASDAQ","currency":"USD","sector":"Automotive","last":0},
    {"name":"BITCOIN","symbol":"BTC-USD","market":"Crypto","currency":"USD","sector":"Crypto","last":0},
    {"name":"ETHEREUM","symbol":"ETH-USD","market":"Crypto","currency":"USD","sector":"Crypto","last":0},
    {"name":"iShares MSCI World","symbol":"IWDA.AS","market":"ETF","currency":"EUR","sector":"ETF","last":0},
    {"name":"Vanguard S&P 500","symbol":"VOO","market":"ETF","currency":"USD","sector":"ETF","last":0},
    {"name":"Amundi NASDAQ-100","symbol":"PANX.PA","market":"ETF FR","currency":"EUR","sector":"ETF","last":0},
]

ALL_ASSETS = EURONEXT_ASSETS + EXTRA_TICKERS

# ─── CATEGORIES ───────────────────────────────────────────────────────────────
ACCOUNT_TYPES   = ["Compte courant","Livret A","LDDS","PEL","CEL","Compte épargne","Compte joint","PEA","Assurance-vie","Compte-titres","Autre"]
INVEST_CATS     = ["Actions françaises","Actions européennes","Actions internationales","ETF monde","ETF sectoriel","ETF obligataire","PEA","Assurance-vie","Crypto-actifs","Obligations","SCPI","Immobilier","Private Equity","Autre"]
EXPENSE_CATS    = ["Alimentation","Logement","Transport","Santé","Loisirs","Restaurants","Vêtements","Éducation","Abonnements","Épargne forcée","Autre"]
BUDGET_PERIODS  = ["Mensuel","Annuel"]

SECTOR_COLORS = {
    "Energy":"#fbbf24","Finance":"#60a5fa","Technology":"#a78bfa","Luxury":"#f472b6",
    "Healthcare":"#34d399","Defense":"#ef4444","Automotive":"#fb923c","Utilities":"#38bdf8",
    "Aerospace":"#e879f9","Consumer":"#4ade80","Materials":"#a8a29e","Media":"#c084fc",
    "Insurance":"#818cf8","Construction":"#d97706","Transportation":"#0ea5e9",
    "Telecom":"#22d3ee","Crypto":"#9b6dff","ETF":"#c9a84c","Autre":"#6b7280"
}

CAT_COLORS = ["#c9a84c","#4a9cff","#27c994","#9270ff","#e8c97a","#f59e0b","#34d399","#60a5fa","#f472b6","#fb923c"]

# ─── PRICE FETCH ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_price(symbol: str):
    """Fetch live price via yfinance, returns (price, change_pct, currency)."""
    try:
        t = yf.Ticker(symbol)
        info = t.fast_info
        price = info.last_price or info.previous_close or 0
        prev  = info.previous_close or price
        chg   = ((price - prev) / prev * 100) if prev else 0
        cur   = getattr(info, "currency", "EUR") or "EUR"
        return round(price, 4), round(chg, 3), cur
    except:
        return 0, 0, "EUR"

@st.cache_data(ttl=300)
def fetch_multiple_prices(symbols: tuple):
    """Batch fetch for ticker tape."""
    results = {}
    for s in symbols:
        p, c, cur = fetch_price(s)
        results[s] = {"price": p, "change": c, "currency": cur}
    return results

def fmt_eur(n):
    if n is None: return "—"
    return f"{n:,.2f} €".replace(",", " ")

def fmt_pct(n):
    if n is None: return "—"
    sign = "+" if n >= 0 else ""
    return f"{sign}{n:.2f}%"

def fmt_num(n):
    return f"{n:,.2f}".replace(",", " ")

# ─── SESSION STATE INIT ───────────────────────────────────────────────────────
if "accounts" not in st.session_state:
    st.session_state.accounts   = load_json(ACCOUNTS_FILE, [])
if "investments" not in st.session_state:
    st.session_state.investments = load_json(INVESTMENTS_FILE, [])
if "expenses" not in st.session_state:
    st.session_state.expenses   = load_json(EXPENSES_FILE, [])
if "budgets" not in st.session_state:
    st.session_state.budgets    = load_json(BUDGETS_FILE, [])
if "goals" not in st.session_state:
    st.session_state.goals      = load_json(GOALS_FILE, [
        {"id":"g1","name":"Épargne cible","target":45000,"current":0,"deadline":"2025-12-31"},
    ])
if "profile" not in st.session_state:
    st.session_state.profile    = load_json(PROFILE_FILE, {"risk":3,"goal":"growth","horizon":5,"name":"Jean Pierre KARL"})
if "prices_cache" not in st.session_state:
    st.session_state.prices_cache = {}

def persist():
    save_json(ACCOUNTS_FILE, st.session_state.accounts)
    save_json(INVESTMENTS_FILE, st.session_state.investments)
    save_json(EXPENSES_FILE, st.session_state.expenses)
    save_json(BUDGETS_FILE, st.session_state.budgets)
    save_json(GOALS_FILE, st.session_state.goals)
    save_json(PROFILE_FILE, st.session_state.profile)

# ─── COMPUTE TOTALS ───────────────────────────────────────────────────────────
def compute_totals():
    t_acc   = sum(float(a.get("value", 0)) for a in st.session_state.accounts)
    t_inv   = sum(float(i.get("value", 0)) for i in st.session_state.investments)
    t_cost  = sum(float(i.get("cost", 0)) for i in st.session_state.investments)
    t_gain  = t_inv - t_cost
    t_gainp = (t_gain / t_cost * 100) if t_cost > 0 else 0
    return {"acc": t_acc, "inv": t_inv, "cost": t_cost, "gain": t_gain, "gainp": t_gainp, "grand": t_acc + t_inv}

def compute_monthly_expenses():
    now = datetime.date.today()
    month_exps = [e for e in st.session_state.expenses
                  if e.get("date","")[:7] == now.strftime("%Y-%m")]
    return sum(float(e.get("amount", 0)) for e in month_exps), month_exps

def check_alerts():
    alerts = []
    T = compute_totals()
    # Goal alerts
    for g in st.session_state.goals:
        cur  = float(g.get("current", 0))
        tgt  = float(g.get("target", 1))
        pct  = cur / tgt * 100 if tgt else 0
        dead = g.get("deadline","")
        if pct < 50 and dead:
            try:
                dl = datetime.date.fromisoformat(dead)
                days = (dl - datetime.date.today()).days
                if days < 180:
                    alerts.append({"type":"error","msg":f"⚠️ Objectif '{g['name']}' : {pct:.0f}% atteint · Échéance dans {days}j"})
            except: pass
        elif pct < 75:
            alerts.append({"type":"warning","msg":f"📊 Objectif '{g['name']}' : {pct:.0f}% atteint ({fmt_eur(cur)} / {fmt_eur(tgt)})"})
    # Budget alerts
    _, month_exps = compute_monthly_expenses()
    total_month = sum(float(e.get("amount",0)) for e in month_exps)
    for b in st.session_state.budgets:
        bcat = b.get("category","")
        blim = float(b.get("limit", 0))
        spent = sum(float(e.get("amount",0)) for e in month_exps if e.get("category") == bcat)
        if blim > 0 and spent > blim * 0.9:
            pct = spent / blim * 100
            alerts.append({"type": "error" if pct > 100 else "warning",
                           "msg": f"{'🚨' if pct>100 else '⚠️'} Budget {bcat} : {fmt_eur(spent)} / {fmt_eur(blim)} ({pct:.0f}%)"})
    # Negative P&L
    if T["gain"] < -500:
        alerts.append({"type":"warning","msg":f"📉 Plus-value négative : {fmt_eur(T['gain'])} ({fmt_pct(T['gainp'])})"})
    return alerts

# ─── PLOTLY THEME ─────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Syne, sans-serif", color="#5a6880"),
    margin=dict(l=10, r=10, t=30, b=10),
    colorway=CAT_COLORS,
)

def make_donut(labels, values, colors=None):
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.72,
        marker=dict(colors=colors or CAT_COLORS[:len(labels)], line=dict(width=0)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>%{value:,.2f} €<br>%{percent}<extra></extra>",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, height=240, showlegend=False)
    return fig

def make_bar(df, x, y, color=None, title=""):
    fig = px.bar(df, x=x, y=y, color=color,
                 color_discrete_sequence=CAT_COLORS,
                 title=title)
    fig.update_layout(**PLOTLY_LAYOUT, height=300, title_font_color="#e8c97a", title_font_size=14)
    fig.update_traces(marker_cornerradius=4)
    return fig

def make_line(df, x, y, title=""):
    fig = px.line(df, x=x, y=y, title=title, markers=True)
    fig.update_layout(**PLOTLY_LAYOUT, height=300, title_font_color="#e8c97a", title_font_size=14)
    fig.update_traces(line_color="#c9a84c", marker_color="#e8c97a", line_width=2)
    return fig

# ─── TICKER TAPE ─────────────────────────────────────────────────────────────
def render_ticker():
    items = []
    for a in EURONEXT_ASSETS[:25]:
        sym  = a["symbol"]
        px_c = st.session_state.prices_cache.get(sym, {})
        price = px_c.get("price", a["last"])
        chg   = px_c.get("change", a["change_pct"])
        color = "#27c994" if chg >= 0 else "#e85252"
        sign  = "▲" if chg >= 0 else "▼"
        items.append(
            f'<span style="margin:0 22px;color:#c9a84c;font-weight:600">{a["symbol"].split(".")[0]}</span>'
            f'<span style="color:#e4e8f0">{price:,.2f}</span>&nbsp;'
            f'<span style="color:{color}">{sign}{abs(chg):.2f}%</span>'
        )
    ticker_html = "".join(items)
    st.markdown(f"""
    <div style="background:rgba(201,168,76,0.05);border-top:1px solid rgba(201,168,76,0.12);
         border-bottom:1px solid rgba(201,168,76,0.12);padding:10px 0;overflow:hidden;
         white-space:nowrap;font-family:'DM Mono',monospace;font-size:12px;margin-bottom:18px">
      <div style="display:inline-block;animation:ticker 60s linear infinite">
        {ticker_html}&nbsp;&nbsp;&nbsp;&nbsp;{ticker_html}
      </div>
    </div>
    <style>@keyframes ticker{{from{{transform:translateX(0)}}to{{transform:translateX(-50%)}}}}</style>
    """, unsafe_allow_html=True)

# ─── HEADER ──────────────────────────────────────────────────────────────────
def render_header():
    now = datetime.datetime.now()
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;
         padding:18px 0 14px;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:18px">
      <div>
        <div class="capital-header">CAPITAL</div>
        <div class="capital-sub">{st.session_state.profile.get('name','—')} · Gestionnaire de Patrimoine</div>
      </div>
      <div style="text-align:right">
        <div style="font-family:'DM Mono',monospace;font-size:22px;color:#e8c97a;font-weight:600">
          {now.strftime('%H:%M')}</div>
        <div style="font-size:11px;color:#5a6880;text-transform:capitalize">
          {now.strftime('%A %d %B %Y')}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:18px 0 12px;border-bottom:1px solid rgba(255,255,255,0.06)">
      <div style="font-family:'Cormorant Garamond',serif;font-size:26px;font-weight:700;color:#e8c97a">CAPITAL</div>
      <div style="font-size:9px;letter-spacing:.2em;color:#5a6880;text-transform:uppercase;margin-top:4px">
        Patrimoine · Investissement</div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    page = st.radio("Navigation", [
        "🏠  Vue Globale",
        "🏦  Comptes Bancaires",
        "📈  Investissements",
        "💸  Dépenses & Budget",
        "🎯  Objectifs",
        "📊  Profil de Risque",
        "🤖  Conseiller IA",
    ], label_visibility="collapsed")

    # Quick totals
    T = compute_totals()
    st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:16px 0'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:9px;letter-spacing:.18em;text-transform:uppercase;color:#5a6880;margin-bottom:10px">Patrimoine</div>
    <div style="font-family:'Cormorant Garamond',serif;font-size:24px;font-weight:700;color:#e8c97a">
      {fmt_eur(T['grand'])}</div>
    <div style="font-size:11px;color:{'#27c994' if T['gain']>=0 else '#e85252'};font-family:'DM Mono',monospace;margin-top:4px">
      {fmt_pct(T['gainp'])} P&L · {fmt_eur(T['gain'])}</div>
    """, unsafe_allow_html=True)

    # Alerts in sidebar
    alerts = check_alerts()
    if alerts:
        st.markdown(f"<hr style='border-color:rgba(255,255,255,0.06);margin:16px 0'>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:9px;letter-spacing:.18em;text-transform:uppercase;color:#e85252;margin-bottom:8px'>🔔 {len(alerts)} alerte(s)</div>", unsafe_allow_html=True)
        for al in alerts[:3]:
            color = "#e85252" if al["type"]=="error" else "#f59e0b"
            st.markdown(f"<div style='font-size:11px;color:{color};margin-bottom:6px;line-height:1.5'>{al['msg']}</div>", unsafe_allow_html=True)

    # Sync prices button
    st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:16px 0'>", unsafe_allow_html=True)
    if st.button("↻  Synchroniser les prix", use_container_width=True, key="sync_btn"):
        with st.spinner("Mise à jour des cours..."):
            syms = tuple(set(
                i.get("ticker","") for i in st.session_state.investments
                if i.get("ticker","").strip()
            ))
            if syms:
                prices = fetch_multiple_prices(syms)
                st.session_state.prices_cache.update(prices)
                # Update investment values
                for inv in st.session_state.investments:
                    tk = inv.get("ticker","")
                    if tk and tk in prices:
                        p = prices[tk]["price"]
                        qty = float(inv.get("qty", 1))
                        inv["value"] = round(p * qty, 2)
                        inv["last_price"] = p
                        inv["last_change"] = prices[tk]["change"]
                persist()
                st.success(f"✅ {len(syms)} actif(s) mis à jour")
            else:
                st.info("Aucun ticker configuré")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: VUE GLOBALE
# ═══════════════════════════════════════════════════════════════════════════════
if "Vue Globale" in page:
    render_header()
    render_ticker()

    # Alerts banner
    alerts = check_alerts()
    for al in alerts:
        if al["type"] == "error":
            st.error(al["msg"])
        else:
            st.warning(al["msg"])

    T = compute_totals()
    _, month_exps = compute_monthly_expenses()
    month_total = sum(float(e.get("amount",0)) for e in month_exps)

    # KPI Row
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Patrimoine Total", fmt_eur(T["grand"]))
    with c2:
        st.metric("Comptes Bancaires", fmt_eur(T["acc"]),
                  delta=f"{len(st.session_state.accounts)} compte(s)")
    with c3:
        st.metric("Investissements", fmt_eur(T["inv"]),
                  delta=f"{len(st.session_state.investments)} position(s)")
    with c4:
        delta_color = "normal" if T["gain"] >= 0 else "inverse"
        st.metric("Plus/Moins-value", fmt_eur(T["gain"]),
                  delta=fmt_pct(T["gainp"]))
    with c5:
        st.metric("Dépenses ce mois", fmt_eur(month_total),
                  delta=f"{len(month_exps)} transaction(s)")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Charts row
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("<div class='section-title'>Répartition du Patrimoine</div>", unsafe_allow_html=True)
        # Build donut data
        labels, values, colors = [], [], []
        if T["acc"] > 0:
            labels.append("Comptes"); values.append(T["acc"]); colors.append("#4a9cff")
        cat_totals = {}
        for inv in st.session_state.investments:
            c = inv.get("category","Autre")
            cat_totals[c] = cat_totals.get(c,0) + float(inv.get("value",0))
        for i,(c,v) in enumerate(sorted(cat_totals.items(), key=lambda x:-x[1])):
            labels.append(c); values.append(v); colors.append(CAT_COLORS[i % len(CAT_COLORS)])

        if values:
            fig = make_donut(labels, values, colors)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
            # Legend
            for lbl, val, col in zip(labels, values, colors):
                pct = val/T["grand"]*100 if T["grand"] else 0
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px">
                  <div style="width:9px;height:9px;border-radius:2px;background:{col};flex-shrink:0"></div>
                  <div style="flex:1;font-size:11px;color:#5a6880">{lbl}</div>
                  <div style="font-family:'DM Mono',monospace;font-size:11px;color:{col}">{pct:.1f}%</div>
                  <div style="font-family:'DM Mono',monospace;font-size:11px;color:#5a6880;min-width:80px;text-align:right">{fmt_eur(val)}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Ajoutez des actifs pour voir la répartition")

    with col_right:
        st.markdown("<div class='section-title'>Top Positions</div>", unsafe_allow_html=True)
        all_items = []
        for acc in st.session_state.accounts:
            all_items.append({
                "Nom": f"🏦 {acc.get('bank','—')} · {acc.get('type','')}",
                "Type": "Compte",
                "Valeur": float(acc.get("value",0)),
                "P&L": "—", "P&L %": "—"
            })
        for inv in st.session_state.investments:
            g  = float(inv.get("value",0)) - float(inv.get("cost",0))
            gp = (g / float(inv.get("cost",1)) * 100) if float(inv.get("cost",0)) > 0 else 0
            all_items.append({
                "Nom": f"◈ {inv.get('name','—')}",
                "Type": inv.get("category","—"),
                "Valeur": float(inv.get("value",0)),
                "P&L": fmt_eur(g),
                "P&L %": fmt_pct(gp)
            })
        all_items.sort(key=lambda x: x["Valeur"], reverse=True)
        if all_items:
            df = pd.DataFrame(all_items[:12])
            df["Valeur"] = df["Valeur"].apply(fmt_eur)
            st.dataframe(df, use_container_width=True, hide_index=True,
                        column_config={"Nom": st.column_config.TextColumn(width="large")})
        else:
            st.info("Aucun actif ajouté")

        # Goals summary
        st.markdown("<div class='section-title' style='margin-top:18px'>Objectifs</div>", unsafe_allow_html=True)
        for g in st.session_state.goals:
            tgt = float(g.get("target",1))
            cur = float(g.get("current",0))
            pct = min(cur/tgt*100, 100) if tgt else 0
            col_g = "#27c994" if pct >= 75 else ("#f59e0b" if pct >= 40 else "#e85252")
            st.markdown(f"""
            <div style="margin-bottom:12px">
              <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                <span style="font-size:12px;font-weight:600">{g.get('name','')}</span>
                <span style="font-family:'DM Mono',monospace;font-size:11px;color:{col_g}">{pct:.0f}%</span>
              </div>
              <div style="height:5px;background:#131820;border-radius:3px;overflow:hidden">
                <div style="height:100%;width:{pct}%;background:{col_g};border-radius:3px;transition:width .5s"></div>
              </div>
              <div style="display:flex;justify-content:space-between;margin-top:4px;font-size:10px;color:#5a6880">
                <span>{fmt_eur(cur)}</span><span>{fmt_eur(tgt)}</span>
              </div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: COMPTES BANCAIRES
# ═══════════════════════════════════════════════════════════════════════════════
elif "Comptes Bancaires" in page:
    render_header()
    st.markdown("<div class='section-title'>Mes Comptes Bancaires</div>", unsafe_allow_html=True)

    total_acc = sum(float(a.get("value",0)) for a in st.session_state.accounts)

    # Summary KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Épargne", fmt_eur(total_acc))
    c2.metric("Nombre de comptes", len(st.session_state.accounts))
    liquid = sum(float(a.get("value",0)) for a in st.session_state.accounts
                 if a.get("type") in ["Compte courant","Compte joint"])
    c3.metric("Liquidités disponibles", fmt_eur(liquid))

    st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:16px 0'>", unsafe_allow_html=True)

    # ─── Existing accounts display
    if st.session_state.accounts:
        cols_per_row = 3
        acc_list = st.session_state.accounts
        for row_start in range(0, len(acc_list), cols_per_row):
            cols = st.columns(cols_per_row)
            for idx, acc in enumerate(acc_list[row_start:row_start+cols_per_row]):
                with cols[idx]:
                    color = CAT_COLORS[row_start+idx % len(CAT_COLORS)]
                    pct = float(acc.get("value",0))/total_acc*100 if total_acc else 0
                    st.markdown(f"""
                    <div class="capital-card" style="border-color:{color}44">
                      <div style="font-size:8px;letter-spacing:.16em;text-transform:uppercase;color:{color};margin-bottom:6px">
                        {acc.get('type','COMPTE').upper()}</div>
                      <div style="font-family:'Cormorant Garamond',serif;font-size:26px;font-weight:700;color:{color}">
                        {fmt_eur(float(acc.get('value',0)))}</div>
                      <div style="font-size:13px;font-weight:600;margin-top:4px">{acc.get('bank','—')}</div>
                      <div style="font-size:11px;color:#5a6880">{acc.get('name','')}</div>
                      {f'<div style="font-size:9px;color:#2a3448;margin-top:8px;font-family:monospace">{acc.get("iban","")}</div>' if acc.get('iban') else ''}
                      <div style="height:4px;background:#131820;border-radius:2px;overflow:hidden;margin-top:10px">
                        <div style="height:100%;width:{pct:.1f}%;background:{color};border-radius:2px"></div>
                      </div>
                      <div style="font-size:9px;color:#5a6880;margin-top:4px">{pct:.1f}% du total</div>
                    </div>
                    """, unsafe_allow_html=True)
                    c_edit, c_del = st.columns(2)
                    if c_edit.button("✎", key=f"edit_acc_{acc['id']}", help="Modifier"):
                        st.session_state[f"edit_acc_id"] = acc["id"]
                    if c_del.button("✕", key=f"del_acc_{acc['id']}", help="Supprimer"):
                        st.session_state.accounts = [a for a in st.session_state.accounts if a["id"] != acc["id"]]
                        persist(); st.rerun()

    # ─── Add / edit form
    edit_id = st.session_state.get("edit_acc_id")
    edit_acc = next((a for a in st.session_state.accounts if a["id"]==edit_id), None) if edit_id else None
    label = "✏️ Modifier le compte" if edit_acc else "➕ Ajouter un compte"

    with st.expander(label, expanded=(edit_acc is not None)):
        with st.form("form_account", clear_on_submit=True):
            col1, col2 = st.columns(2)
            bank = col1.text_input("Banque", value=edit_acc.get("bank","") if edit_acc else "")
            name = col2.text_input("Nom du compte", value=edit_acc.get("name","") if edit_acc else "")
            col3, col4 = st.columns(2)
            atype_idx = ACCOUNT_TYPES.index(edit_acc["type"]) if edit_acc and edit_acc.get("type") in ACCOUNT_TYPES else 0
            atype = col3.selectbox("Type", ACCOUNT_TYPES, index=atype_idx)
            value = col4.number_input("Solde (€)", min_value=0.0, step=0.01,
                                      value=float(edit_acc.get("value",0)) if edit_acc else 0.0)
            iban = st.text_input("IBAN (optionnel)", value=edit_acc.get("iban","") if edit_acc else "")
            submit = st.form_submit_button("💾 Enregistrer", type="primary", use_container_width=True)
            if submit:
                if not bank:
                    st.error("La banque est requise.")
                else:
                    item = {"id": edit_id or str(int(time.time()*1000)),
                            "bank":bank, "name":name, "type":atype,
                            "value":value, "iban":iban}
                    if edit_id:
                        st.session_state.accounts = [item if a["id"]==edit_id else a
                                                      for a in st.session_state.accounts]
                        st.session_state.pop("edit_acc_id", None)
                    else:
                        st.session_state.accounts.append(item)
                    persist(); st.rerun()

    # Bar chart
    if st.session_state.accounts:
        st.markdown("<div class='section-title' style='margin-top:18px'>Répartition des comptes</div>", unsafe_allow_html=True)
        df_acc = pd.DataFrame([{"Compte": f"{a['bank']} · {a.get('type','')}", "Solde": float(a.get("value",0))}
                                for a in st.session_state.accounts])
        fig = go.Figure(go.Bar(
            x=df_acc["Solde"], y=df_acc["Compte"], orientation="h",
            marker=dict(color=CAT_COLORS[:len(df_acc)], cornerradius=5),
            hovertemplate="<b>%{y}</b><br>%{x:,.2f} €<extra></extra>"
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=max(220, len(df_acc)*55))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: INVESTISSEMENTS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Investissements" in page:
    render_header()
    render_ticker()
    st.markdown("<div class='section-title'>Actions, ETF & Investissements</div>", unsafe_allow_html=True)

    T = compute_totals()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Investi", fmt_eur(T["inv"]))
    c2.metric("Coût Total", fmt_eur(T["cost"]))
    c3.metric("Plus/Moins-value", fmt_eur(T["gain"]), delta=fmt_pct(T["gainp"]))
    c4.metric("Positions ouvertes", len(st.session_state.investments))

    st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:16px 0'>", unsafe_allow_html=True)

    # ─── Investments table
    if st.session_state.investments:
        rows = []
        for inv in st.session_state.investments:
            val  = float(inv.get("value",0))
            cost = float(inv.get("cost",0))
            g    = val - cost
            gp   = g/cost*100 if cost > 0 else 0
            chg_day = inv.get("last_change", None)
            rows.append({
                "Actif": inv.get("name","—"),
                "Catégorie": inv.get("category","—"),
                "Ticker": inv.get("ticker","—"),
                "Qté": inv.get("qty","—"),
                "Valeur": fmt_eur(val),
                "Coût": fmt_eur(cost),
                "+/-  Val.": fmt_eur(g),
                "Perf.": fmt_pct(gp),
                "Jour": fmt_pct(chg_day) if chg_day is not None else "—",
            })
        df_inv = pd.DataFrame(rows)
        st.dataframe(df_inv, use_container_width=True, hide_index=True,
                     column_config={
                         "Perf.": st.column_config.TextColumn(),
                         "Actif": st.column_config.TextColumn(width="medium"),
                     })

        # Chart: by category
        cat_totals = {}
        for inv in st.session_state.investments:
            c = inv.get("category","Autre")
            cat_totals[c] = cat_totals.get(c,0) + float(inv.get("value",0))

        col_d, col_perf = st.columns(2)
        with col_d:
            st.markdown("<div class='section-title'>Par catégorie</div>", unsafe_allow_html=True)
            fig = make_donut(list(cat_totals.keys()), list(cat_totals.values()))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

        with col_perf:
            st.markdown("<div class='section-title'>Performance</div>", unsafe_allow_html=True)
            perf_rows = []
            for inv in st.session_state.investments:
                val  = float(inv.get("value",0))
                cost = float(inv.get("cost",0))
                gp   = (val-cost)/cost*100 if cost > 0 else 0
                perf_rows.append({"Actif": inv.get("name","")[:18], "Perf (%)": round(gp,2)})
            if perf_rows:
                df_p = pd.DataFrame(perf_rows).sort_values("Perf (%)", ascending=True)
                fig2 = go.Figure(go.Bar(
                    x=df_p["Perf (%)"], y=df_p["Actif"], orientation="h",
                    marker=dict(color=["#27c994" if v>=0 else "#e85252" for v in df_p["Perf (%)"]], cornerradius=4),
                ))
                fig2.update_layout(**PLOTLY_LAYOUT, height=max(220, len(df_p)*45))
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})

    # ─── Add / edit form
    edit_id  = st.session_state.get("edit_inv_id")
    edit_inv = next((i for i in st.session_state.investments if i["id"]==edit_id), None) if edit_id else None
    label = "✏️ Modifier la position" if edit_inv else "➕ Ajouter une position"

    # Ticker search helper
    st.markdown("---")
    st.markdown("<div style='font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#5a6880;margin-bottom:8px'>Rechercher un actif Euronext / Yahoo</div>", unsafe_allow_html=True)
    search_q = st.text_input("Ticker ou nom", placeholder="MC.PA, ASML, LVMH, BTC-USD…", label_visibility="collapsed", key="inv_search")
    if search_q:
        matches = [a for a in ALL_ASSETS if search_q.upper() in a["symbol"].upper() or search_q.upper() in a["name"].upper()][:10]
        if matches:
            sel = st.selectbox("Résultats", [f"{a['symbol']} — {a['name']} ({a['market']})" for a in matches],
                               key="inv_sel", label_visibility="collapsed")
            if sel and st.button("📥 Pré-remplir le formulaire"):
                idx = [f"{a['symbol']} — {a['name']} ({a['market']})" for a in matches].index(sel)
                chosen = matches[idx]
                st.session_state["prefill_ticker"] = chosen["symbol"]
                st.session_state["prefill_name"]   = chosen["name"]
                st.session_state["prefill_cat"]     = "ETF monde" if chosen["sector"]=="ETF" else (
                                                       "Crypto-actifs" if chosen["sector"]=="Crypto" else
                                                       "Actions françaises" if "Paris" in chosen["market"] else "Actions européennes")
                # fetch live price
                p, c_day, cur = fetch_price(chosen["symbol"])
                st.session_state["prefill_price"] = p
                st.info(f"Prix actuel : {p:.4f} {cur} · Variation jour : {fmt_pct(c_day)}")

    with st.expander(label, expanded=(edit_inv is not None)):
        with st.form("form_inv", clear_on_submit=True):
            col1, col2 = st.columns(2)
            default_name   = st.session_state.get("prefill_name", edit_inv.get("name","") if edit_inv else "")
            default_ticker = st.session_state.get("prefill_ticker", edit_inv.get("ticker","") if edit_inv else "")
            default_cat    = st.session_state.get("prefill_cat", edit_inv.get("category","Actions françaises") if edit_inv else "Actions françaises")
            default_price  = st.session_state.get("prefill_price", float(edit_inv.get("value",0)) if edit_inv else 0.0)

            name   = col1.text_input("Nom de l'actif", value=default_name)
            ticker = col2.text_input("Ticker Yahoo Finance", value=default_ticker, placeholder="MC.PA, ASML, BTC-USD…")

            col3, col4 = st.columns(2)
            cat_idx = INVEST_CATS.index(default_cat) if default_cat in INVEST_CATS else 0
            cat  = col3.selectbox("Catégorie", INVEST_CATS, index=cat_idx)
            issuer = col4.text_input("Plateforme / Émetteur", value=edit_inv.get("issuer","") if edit_inv else "")

            col5, col6, col7 = st.columns(3)
            qty   = col5.number_input("Quantité", min_value=0.0, step=0.001,
                                       value=float(edit_inv.get("qty",1)) if edit_inv else 1.0)
            value = col6.number_input("Valeur actuelle (€)", min_value=0.0, step=0.01,
                                       value=default_price if not edit_inv else float(edit_inv.get("value",0)))
            cost  = col7.number_input("Prix de revient (€)", min_value=0.0, step=0.01,
                                       value=float(edit_inv.get("cost",0)) if edit_inv else 0.0)
            notes = st.text_area("Notes / stratégie", value=edit_inv.get("notes","") if edit_inv else "", height=70)

            submit = st.form_submit_button("💾 Enregistrer", type="primary", use_container_width=True)
            if submit:
                if not name:
                    st.error("Le nom est requis.")
                else:
                    item = {
                        "id": edit_id or str(int(time.time()*1000)),
                        "name":name, "category":cat, "ticker":ticker,
                        "issuer":issuer, "qty":qty, "value":value,
                        "cost":cost, "notes":notes
                    }
                    if edit_id:
                        st.session_state.investments = [item if i["id"]==edit_id else i
                                                        for i in st.session_state.investments]
                        st.session_state.pop("edit_inv_id",None)
                    else:
                        st.session_state.investments.append(item)
                    for k in ["prefill_ticker","prefill_name","prefill_cat","prefill_price"]:
                        st.session_state.pop(k, None)
                    persist(); st.rerun()

    # Delete buttons
    if st.session_state.investments:
        st.markdown("<div style='font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#5a6880;margin-bottom:8px;margin-top:12px'>Gérer les positions</div>", unsafe_allow_html=True)
        for inv in st.session_state.investments:
            c_n, c_e, c_d = st.columns([4,1,1])
            c_n.markdown(f"<span style='font-size:13px'>◈ {inv.get('name','—')} <span style='color:#5a6880;font-size:10px'>{inv.get('ticker','')}</span></span>", unsafe_allow_html=True)
            if c_e.button("✎", key=f"edit_inv_{inv['id']}"):
                st.session_state["edit_inv_id"] = inv["id"]; st.rerun()
            if c_d.button("✕", key=f"del_inv_{inv['id']}"):
                st.session_state.investments = [i for i in st.session_state.investments if i["id"]!=inv["id"]]
                persist(); st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DÉPENSES & BUDGET
# ═══════════════════════════════════════════════════════════════════════════════
elif "Dépenses" in page:
    render_header()
    st.markdown("<div class='section-title'>Dépenses Quotidiennes & Budgets</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋  Saisie dépenses", "📊  Analyse", "⚙️  Budgets"])

    # ─── TAB 1: Add expense
    with tab1:
        now = datetime.date.today()
        _, month_exps = compute_monthly_expenses()
        month_total = sum(float(e.get("amount",0)) for e in month_exps)

        c1, c2, c3 = st.columns(3)
        c1.metric("Dépenses ce mois", fmt_eur(month_total))
        c2.metric("Transactions", len(month_exps))
        # Budget vs actual
        total_budget = sum(float(b.get("limit",0)) for b in st.session_state.budgets
                          if b.get("period","Mensuel")=="Mensuel")
        if total_budget:
            c3.metric("Budget restant", fmt_eur(total_budget - month_total),
                     delta=fmt_pct((total_budget-month_total)/total_budget*100) if total_budget else "—")

        st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:16px 0'>", unsafe_allow_html=True)

        # Add expense form
        with st.form("form_expense", clear_on_submit=True):
            st.markdown("<div style='font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#5a6880;margin-bottom:10px'>Nouvelle dépense</div>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns([2,1,2,2])
            desc   = col1.text_input("Description", placeholder="Courses, Loyer, Métro…")
            amount = col2.number_input("Montant (€)", min_value=0.01, step=0.01)
            cat    = col3.selectbox("Catégorie", EXPENSE_CATS)
            date   = col4.date_input("Date", value=now)
            submit = st.form_submit_button("➕ Ajouter", type="primary", use_container_width=True)
            if submit:
                if desc and amount > 0:
                    st.session_state.expenses.append({
                        "id": str(int(time.time()*1000)),
                        "description": desc, "amount": amount,
                        "category": cat, "date": str(date)
                    })
                    persist(); st.rerun()

        # Recent expenses
        if st.session_state.expenses:
            st.markdown("<div class='section-title' style='margin-top:16px'>Transactions récentes</div>", unsafe_allow_html=True)
            recent = sorted(st.session_state.expenses, key=lambda e: e.get("date",""), reverse=True)[:50]
            for exp in recent:
                c_d, c_cat, c_amt, c_del = st.columns([3,2,1,1])
                c_d.markdown(f"<span style='font-size:13px'>{exp.get('description','—')}</span><br><span style='font-size:10px;color:#5a6880'>{exp.get('date','')}</span>", unsafe_allow_html=True)
                c_cat.markdown(f"<span style='font-size:11px;color:#c9a84c'>{exp.get('category','')}</span>", unsafe_allow_html=True)
                c_amt.markdown(f"<span style='font-size:13px;color:#e85252;font-family:DM Mono'>{fmt_eur(float(exp.get('amount',0)))}</span>", unsafe_allow_html=True)
                if c_del.button("✕", key=f"del_exp_{exp['id']}"):
                    st.session_state.expenses = [e for e in st.session_state.expenses if e["id"]!=exp["id"]]
                    persist(); st.rerun()

    # ─── TAB 2: Analysis
    with tab2:
        if not st.session_state.expenses:
            st.info("Ajoutez des dépenses pour voir l'analyse")
        else:
            df_exp = pd.DataFrame(st.session_state.expenses)
            df_exp["amount"] = pd.to_numeric(df_exp["amount"], errors="coerce")
            df_exp["date"] = pd.to_datetime(df_exp["date"])
            df_exp["month"] = df_exp["date"].dt.to_period("M").astype(str)

            col_l, col_r = st.columns(2)
            with col_l:
                st.markdown("<div class='section-title'>Par catégorie (total)</div>", unsafe_allow_html=True)
                by_cat = df_exp.groupby("category")["amount"].sum().reset_index()
                fig = make_donut(by_cat["category"].tolist(), by_cat["amount"].tolist())
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

            with col_r:
                st.markdown("<div class='section-title'>Évolution mensuelle</div>", unsafe_allow_html=True)
                by_month = df_exp.groupby("month")["amount"].sum().reset_index()
                fig2 = make_line(by_month, "month", "amount", "")
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})

            st.markdown("<div class='section-title'>Dépenses par catégorie et par mois</div>", unsafe_allow_html=True)
            pivot = df_exp.pivot_table(values="amount", index="month", columns="category", aggfunc="sum", fill_value=0)
            fig3 = go.Figure()
            for i, cat in enumerate(pivot.columns):
                fig3.add_trace(go.Bar(name=cat, x=pivot.index.tolist(), y=pivot[cat].tolist(),
                                      marker_color=CAT_COLORS[i % len(CAT_COLORS)]))
            fig3.update_layout(**PLOTLY_LAYOUT, barmode="stack", height=350)
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})

    # ─── TAB 3: Budgets
    with tab3:
        st.markdown("<div class='section-title'>Gérer les Budgets</div>", unsafe_allow_html=True)

        # Budget vs actual
        if st.session_state.budgets:
            _, month_exps = compute_monthly_expenses()
            for b in st.session_state.budgets:
                blim  = float(b.get("limit",0))
                bcat  = b.get("category","")
                spent = sum(float(e.get("amount",0)) for e in month_exps if e.get("category")==bcat)
                pct   = min(spent/blim*100, 100) if blim else 0
                over  = spent > blim
                col_b = "#e85252" if over else ("#f59e0b" if pct > 75 else "#27c994")
                c_n, c_del = st.columns([5,1])
                with c_n:
                    st.markdown(f"""
                    <div style="margin-bottom:14px">
                      <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                        <span style="font-size:13px;font-weight:600">{bcat}</span>
                        <span style="font-family:'DM Mono',monospace;font-size:12px;color:{col_b}">
                          {fmt_eur(spent)} / {fmt_eur(blim)} · {pct:.0f}%</span>
                      </div>
                      <div style="height:5px;background:#131820;border-radius:3px;overflow:hidden">
                        <div style="height:100%;width:{pct:.1f}%;background:{col_b};border-radius:3px"></div>
                      </div>
                      {'<div style="font-size:10px;color:#e85252;margin-top:3px">⚠️ Dépassement de budget</div>' if over else ''}
                    </div>""", unsafe_allow_html=True)
                if c_del.button("✕", key=f"del_bud_{b['id']}"):
                    st.session_state.budgets = [x for x in st.session_state.budgets if x["id"]!=b["id"]]
                    persist(); st.rerun()

        # Add budget
        with st.expander("➕ Ajouter un budget"):
            with st.form("form_budget", clear_on_submit=True):
                col1, col2 = st.columns(2)
                bcat  = col1.selectbox("Catégorie", EXPENSE_CATS)
                blim  = col2.number_input("Plafond mensuel (€)", min_value=1.0, step=5.0)
                submit = st.form_submit_button("💾 Créer le budget", type="primary", use_container_width=True)
                if submit:
                    # replace if exists
                    st.session_state.budgets = [b for b in st.session_state.budgets if b.get("category")!=bcat]
                    st.session_state.budgets.append({
                        "id": str(int(time.time()*1000)),
                        "category": bcat, "limit": blim, "period":"Mensuel"
                    })
                    persist(); st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: OBJECTIFS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Objectifs" in page:
    render_header()
    st.markdown("<div class='section-title'>Mes Objectifs Financiers</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:12px;color:#5a6880;margin-bottom:18px'>Définissez vos objectifs et suivez votre progression. Des alertes automatiques vous notifient en cas de retard.</div>", unsafe_allow_html=True)

    for g in st.session_state.goals:
        tgt  = float(g.get("target",1))
        cur  = float(g.get("current",0))
        pct  = min(cur/tgt*100, 100) if tgt else 0
        dead = g.get("deadline","")
        col_g = "#27c994" if pct >= 75 else ("#f59e0b" if pct >= 40 else "#e85252")

        days_left = None
        if dead:
            try:
                dl = datetime.date.fromisoformat(dead)
                days_left = (dl - datetime.date.today()).days
            except: pass

        c_info, c_del = st.columns([5,1])
        with c_info:
            st.markdown(f"""
            <div class="capital-card">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">
                <div>
                  <div style="font-family:'Cormorant Garamond',serif;font-size:20px;font-weight:700">{g.get('name','')}</div>
                  {f'<div style="font-size:10px;color:#5a6880">Échéance : {dead}{f" · {days_left}j restants" if days_left is not None else ""}</div>' if dead else ''}
                </div>
                <div style="text-align:right">
                  <div style="font-family:'Cormorant Garamond',serif;font-size:22px;font-weight:700;color:{col_g}">{pct:.0f}%</div>
                </div>
              </div>
              <div style="display:flex;justify-content:space-between;margin-bottom:6px;font-size:12px">
                <span style="color:#5a6880">Atteint : <b style="color:{col_g}">{fmt_eur(cur)}</b></span>
                <span style="color:#5a6880">Objectif : <b style="color:#e8c97a">{fmt_eur(tgt)}</b></span>
              </div>
              <div style="height:8px;background:#131820;border-radius:4px;overflow:hidden">
                <div style="height:100%;width:{pct:.1f}%;background:linear-gradient(90deg,{col_g},{col_g}99);border-radius:4px;transition:width .6s"></div>
              </div>
              {f'<div class="alert-box" style="margin-top:10px;margin-bottom:0">⚠️ Objectif en retard — {days_left}j restants pour {fmt_eur(tgt-cur)} manquants</div>' if days_left is not None and days_left < 90 and pct < 80 else ''}
            </div>""", unsafe_allow_html=True)
            # Update current
            new_cur = st.number_input(f"Mettre à jour : {g.get('name','')}",
                                       min_value=0.0, value=cur, step=100.0,
                                       key=f"goal_cur_{g['id']}")
            if new_cur != cur:
                for gg in st.session_state.goals:
                    if gg["id"] == g["id"]:
                        gg["current"] = new_cur
                persist()

        if c_del.button("✕", key=f"del_goal_{g['id']}"):
            st.session_state.goals = [x for x in st.session_state.goals if x["id"]!=g["id"]]
            persist(); st.rerun()

    # Add goal
    with st.expander("➕ Nouvel objectif"):
        with st.form("form_goal", clear_on_submit=True):
            col1, col2 = st.columns(2)
            gname  = col1.text_input("Nom de l'objectif", placeholder="Épargne cible, Apport immobilier…")
            gtarget = col2.number_input("Montant cible (€)", min_value=100.0, step=500.0)
            col3, col4 = st.columns(2)
            gcurrent = col3.number_input("Montant actuel (€)", min_value=0.0, step=100.0)
            gdeadline = col4.date_input("Échéance", value=datetime.date.today()+datetime.timedelta(days=365))
            submit = st.form_submit_button("💾 Créer l'objectif", type="primary", use_container_width=True)
            if submit and gname:
                st.session_state.goals.append({
                    "id": str(int(time.time()*1000)),
                    "name": gname, "target": gtarget,
                    "current": gcurrent, "deadline": str(gdeadline)
                })
                persist(); st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: PROFIL DE RISQUE
# ═══════════════════════════════════════════════════════════════════════════════
elif "Profil de Risque" in page:
    render_header()
    st.markdown("<div class='section-title'>Profil d'Investisseur</div>", unsafe_allow_html=True)

    prof = st.session_state.profile
    RISK_LABELS = {1:"Défensif",2:"Prudent",3:"Équilibré",4:"Dynamique",5:"Agressif"}
    GOAL_LABELS = {"capital":"Préserver le capital","income":"Revenus réguliers",
                   "growth":"Croissance patrimoniale","speculative":"Spéculatif"}

    col_q, col_res = st.columns([1, 1])

    with col_q:
        st.markdown("<div style='font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#5a6880;margin-bottom:14px'>Questionnaire</div>", unsafe_allow_html=True)
        with st.form("form_profile"):
            pname = st.text_input("Votre nom", value=prof.get("name","Jean Pierre KARL"))
            risk  = st.slider("Tolérance au risque", 1, 5, value=int(prof.get("risk",3)),
                              format="%d",
                              help="1=Défensif · 3=Équilibré · 5=Agressif")
            st.caption(f"**{RISK_LABELS.get(risk,'—')}** — Niveau {risk}/5")

            goal  = st.selectbox("Objectif principal", list(GOAL_LABELS.keys()),
                                  index=list(GOAL_LABELS.keys()).index(prof.get("goal","growth")),
                                  format_func=lambda x: GOAL_LABELS[x])
            horizon = st.select_slider("Horizon d'investissement",
                                        options=[1,3,5,10,20],
                                        value=int(prof.get("horizon",5)),
                                        format_func=lambda x: f"{x} an{'s' if x>1 else ''}")
            submit = st.form_submit_button("💾 Sauvegarder", type="primary", use_container_width=True)
            if submit:
                st.session_state.profile.update({"name":pname,"risk":risk,"goal":goal,"horizon":horizon})
                persist(); st.rerun()

    with col_res:
        risk_cur = int(prof.get("risk",3))
        col = ["#4a9cff","#27c994","#c9a84c","#f59e0b","#e85252"][risk_cur-1]
        RISK_DESC = {
            1:"Vous prioritisez la préservation du capital. Portefeuille recommandé : 40% obligations, 35% actions défensives, 25% monétaire.",
            2:"Équilibre sécurité/rendement. Portefeuille : 30% ETF monde, 30% actions solides, 25% obligations, 15% immobilier.",
            3:"Croissance à long terme. Portefeuille : 40% ETF monde, 30% actions croissance, 15% obligations, 15% alternatif.",
            4:"Croissance dynamique. Portefeuille : 45% actions tech/growth, 30% ETF sectoriels, 25% actifs risqués.",
            5:"Maximiser les gains. Portefeuille : 40% actions spéculatives, 35% crypto, 25% levier/options.",
        }
        ALLOC_DATA = {
            1:[("Obligations",40,"#818cf8"),("Actions défensives",35,"#4a9cff"),("Monétaire",25,"#27c994")],
            2:[("ETF monde",30,"#4a9cff"),("Actions",30,"#c9a84c"),("Obligations",25,"#818cf8"),("Immobilier",15,"#27c994")],
            3:[("ETF monde",40,"#4a9cff"),("Actions",30,"#c9a84c"),("Obligations",15,"#818cf8"),("Alternatif",15,"#9270ff")],
            4:[("Actions Tech",45,"#c9a84c"),("ETF sectoriels",30,"#4a9cff"),("Actifs risqués",25,"#e85252")],
            5:[("Actions Spéc.",40,"#c9a84c"),("Crypto",35,"#9270ff"),("Levier",25,"#e85252")],
        }

        st.markdown(f"""
        <div class="capital-card" style="border-color:{col}44">
          <div style="display:inline-block;background:{col};color:#07090d;font-weight:700;
               font-size:12px;padding:4px 14px;border-radius:8px;margin-bottom:10px">
            Profil {RISK_LABELS.get(risk_cur,'—')}</div>
          <div style="font-family:'Cormorant Garamond',serif;font-size:26px;font-weight:700;
               color:{col};margin-bottom:8px">{RISK_LABELS.get(risk_cur,'—')}</div>
          <div style="font-size:12px;color:#5a6880;line-height:1.65;margin-bottom:16px">
            {RISK_DESC.get(risk_cur,'')}</div>
        </div>""", unsafe_allow_html=True)

        alloc = ALLOC_DATA.get(risk_cur, [])
        for cat, pct, c in alloc:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
              <div style="font-size:11px;width:130px;color:#5a6880">{cat}</div>
              <div style="flex:1;height:6px;background:#131820;border-radius:3px;overflow:hidden">
                <div style="height:100%;width:{pct}%;background:{c};border-radius:3px"></div>
              </div>
              <div style="font-family:'DM Mono',monospace;font-size:11px;color:{c};width:34px;text-align:right">{pct}%</div>
            </div>""", unsafe_allow_html=True)

        # Suggested stocks from Euronext based on profile
        st.markdown("<div class='section-title' style='margin-top:16px'>Titres suggérés</div>", unsafe_allow_html=True)
        SUGGESTIONS = {
            1:["TTE.PA","BNP.PA","ORA.PA","ENEL.MI","GLE.PA"],
            2:["MC.PA","SAN.PA","AIR.PA","ASML","OR.PA"],
            3:["ASML","RMS.PA","SU.PA","DSY.PA","CAP.PA"],
            4:["KOG.OL","SAF.PA","STM.PA","NVDA","TSLA"],
            5:["BTC-USD","ETH-USD","NVDA","MSTR","COIN"],
        }
        for sym in SUGGESTIONS.get(risk_cur, []):
            asset = next((a for a in ALL_ASSETS if a["symbol"]==sym), None)
            if asset:
                price = asset.get("last", 0)
                st.markdown(f"<div style='display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:12px'><span><b>{asset['name']}</b> <span style='color:#5a6880;font-family:DM Mono'>{sym}</span></span><span style='color:{col};font-family:DM Mono'>{price:,.2f} {asset['currency']}</span></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: CONSEILLER IA
# ═══════════════════════════════════════════════════════════════════════════════
elif "Conseiller IA" in page:
    render_header()
    st.markdown("<div class='section-title'>Conseiller IA Patrimonial</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:12px;color:#5a6880;margin-bottom:16px;line-height:1.7'>Analyse personnalisée de votre patrimoine. Le conseiller accède à tous vos comptes, positions et objectifs pour vous répondre précisément.</div>", unsafe_allow_html=True)

    T = compute_totals()
    _, month_exps = compute_monthly_expenses()
    month_total = sum(float(e.get("amount",0)) for e in month_exps)
    prof = st.session_state.profile
    RISK_LABELS = {1:"Défensif",2:"Prudent",3:"Équilibré",4:"Dynamique",5:"Agressif"}

    context = f"""Tu es un conseiller financier expert et bienveillant pour {prof.get('name','Jean Pierre KARL')}.

PATRIMOINE :
- Patrimoine total : {T['grand']:,.2f} €
- Comptes bancaires : {T['acc']:,.2f} € ({len(st.session_state.accounts)} comptes)
- Investissements : {T['inv']:,.2f} € ({len(st.session_state.investments)} positions)
- Plus-value latente : {T['gain']:,.2f} € ({T['gainp']:.2f}%)
- Dépenses ce mois : {month_total:,.2f} €

PROFIL :
- Risque : {RISK_LABELS.get(int(prof.get('risk',3)),'Équilibré')} ({prof.get('risk',3)}/5)
- Objectif : {prof.get('goal','growth')}
- Horizon : {prof.get('horizon',5)} ans

COMPTES : {json.dumps([{'bank':a.get('bank'),'type':a.get('type'),'value':a.get('value')} for a in st.session_state.accounts], ensure_ascii=False)}

INVESTISSEMENTS : {json.dumps([{'name':i.get('name'),'category':i.get('category'),'value':i.get('value'),'cost':i.get('cost')} for i in st.session_state.investments], ensure_ascii=False)}

OBJECTIFS : {json.dumps([{'name':g.get('name'),'target':g.get('target'),'current':g.get('current'),'deadline':g.get('deadline')} for g in st.session_state.goals], ensure_ascii=False)}

Règles : Réponds en FRANÇAIS. Sois direct, concis (max 250 mots), personnalisé et actionnable. Donne des chiffres concrets."""

    # Quick chips
    chips = [
        "Analyse complète de mon patrimoine",
        "Comment atteindre mes objectifs ?",
        "Optimiser ma fiscalité",
        "Mon profil de risque est-il adapté ?",
        "Recommande des ETF pour mon profil",
        "Stratégie d'épargne mensuelle",
    ]
    cols_chips = st.columns(3)
    for i, chip in enumerate(chips):
        if cols_chips[i%3].button(chip, key=f"chip_{i}", use_container_width=True):
            st.session_state["ai_prefill"] = chip

    # Chat input
    question = st.text_area(
        "Votre question",
        value=st.session_state.get("ai_prefill",""),
        placeholder="Ex: Comment diversifier mon portefeuille ? Dois-je ouvrir un PEA ?",
        height=90,
        label_visibility="collapsed",
        key="ai_question_input"
    )

    if st.button("🔍 Analyser", type="primary", use_container_width=True):
        if question.strip():
            st.session_state.pop("ai_prefill", None)
            try:
                import anthropic
                client = anthropic.Anthropic()
                with st.spinner("Analyse en cours..."):
                    msg = client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=1000,
                        system=context,
                        messages=[{"role":"user","content":question}]
                    )
                    answer = msg.content[0].text
                st.markdown(f"""
                <div style="background:rgba(201,168,76,0.05);border:1px solid rgba(201,168,76,0.15);
                     border-radius:16px;padding:20px;margin-top:16px">
                  <div style="font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:#c9a84c;
                       margin-bottom:12px;display:flex;align-items:center;gap:6px">
                    <div style="width:7px;height:7px;border-radius:50%;background:#e8c97a"></div>
                    Conseiller IA · {datetime.datetime.now().strftime('%H:%M')}
                  </div>
                  <div style="font-size:11px;color:#c9a84c;opacity:.7;font-style:italic;margin-bottom:10px">
                    "{question[:80]}{'...' if len(question)>80 else ''}"</div>
                  <div style="font-family:Georgia,serif;font-size:14px;line-height:1.8;color:#d4c49a;
                       white-space:pre-wrap">{answer}</div>
                </div>
                """, unsafe_allow_html=True)
            except ImportError:
                st.error("❌ Package `anthropic` non installé. Ajoutez `anthropic` à requirements.txt")
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
        else:
            st.warning("Saisissez une question")

    # Context summary
    with st.expander("📋 Contexte transmis au conseiller"):
        st.code(context, language="text")
