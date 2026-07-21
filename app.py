import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from src.ml_model import HockeyPredictorML
from src.logos import get_team_logo
from src.schedule import get_upcoming_matches

def get_ml_predictor(df_data):


    model = HockeyPredictorML()
    model.train(df_data)
    return model



# Page configuration
st.set_page_config(
    page_title="Overtime Analytics - Premium Hockey Dashboard",
    page_icon="🏒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling
st.markdown("""
<style>
    /* Premium Header */
    .main-title {
        font-family: 'Outfit', 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8F8F 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: var(--text-color);
        opacity: 0.8;
        margin-bottom: 2rem;
    }
    
    /* Metrics styling */
    .metric-card {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        text-align: center;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #FF4B4B;
        box-shadow: 0 8px 30px rgba(255, 75, 75, 0.15);
    }
    .metric-val {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--text-color);
        margin: 0.5rem 0;
    }
    .metric-lbl {
        font-size: 0.9rem;
        color: var(--text-color);
        opacity: 0.7;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Calculator Container */
    .calc-container {
        background-color: var(--secondary-background-color);
        border: 1px dashed #FF4B4B;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 30px rgba(255, 75, 75, 0.05);
        margin-top: 1rem;
    }
    
    /* Metric Help Tooltip Icon */
    .help-icon {
        display: inline-block;
        margin-left: 4px;
        font-size: 0.75rem;
        color: var(--text-color);
        opacity: 0.6;
        cursor: help;
        border: 1px solid currentColor;
        border-radius: 50%;
        width: 15px;
        height: 15px;
        line-height: 13px;
        text-align: center;
        font-weight: bold;
        vertical-align: middle;
    }
    .help-icon:hover {
        opacity: 1.0;
        color: #FF4B4B;
        border-color: #FF4B4B;
    }
    
    /* Button styling - softer color & contrast readability */
    .stButton > button[kind="primary"], div.stButton > button {
        background-color: #2E3A4E !important;
        color: #F0F6FC !important;
        border: 1px solid #4A5D78 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton > button[kind="primary"]:hover, div.stButton > button:hover {
        background-color: #3B4C66 !important;
        border-color: #38BDF8 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)



# Translation dictionary
t = {
    "CZ": {
        "title": "Hokejový Analytický Dashboard",
        "subtitle": "Prémiové statistiky, klasifikace ligy a analýza historických trendů",
        "total_teams": "Celkem týmů",
        "total_seasons": "Celkem sezón",
        "total_goals": "Góly celkem",
        "avg_win_pct": "Průměrná výhra %",
        "visualizations": "Vizualizace výkonu ligy",
        "correlation": "Korelace mezi vstřelenými góly a výhrami",
        "goals_scored": "Vstřelené góly (GF)",
        "wins": "Výhry",
        "losses": "Prohry",
        "victories_by_league": "Počet výher podle ligové kategorie",
        "league_group": "Ligová skupina",
        "team_trend": "Historická analýza týmu",
        "select_team": "Vyberte tým pro analýzu trendů",
        "matches_count": "Počet zápasů",
        "season": "Sezóna",
        "model_properties": "Vlastnosti modelu",
        "margin": "Marže bookmakera (%)",
        "simulator_title": "Simulátor sázkových kurzů",
        "simulator_desc": "Simulujte pravděpodobnost zápasů a zobrazte sázkové kurzy s marží",
        "home_team": "Domácí tým",
        "away_team": "Hostující tým",
        "warn_different": "Vyberte prosím dva různé týmy pro výpočet kurzů.",
        "probabilities": "Pravděpodobnosti výsledků",
        "win_probability": "Pravděpodobnost výhry",
        "suggested_odds": "Doporučené sázkové kurzy",
        "decimal_odd_home": "Desetinný kurz pro {team} (Domácí)",
        "decimal_odd_away": "Desetinný kurz pro {team} (Hosté)",
        "raw_odd": "Čistý kurz: {odd:.2f}",
        "odd_label": "Kurz: {odd:.2f}",
        "h2h_title": "Historické vzájemné statistiky",
        "metric_col": "Metrika",
        "total_wins_label": "Celkem výher",
        "total_losses_label": "Celkem proher",
        "goals_scored_label": "Vstřelené góly",
        "goals_conceded_label": "Obdržené góly",
        "raw_explorer": "Průzkumník hrubých dat",
        "raw_explorer_desc": "Vyhledávejte, filtrujte a kontrolujte kompletní zpracovaná data",
        "search_team": "Hledat název týmu",
        "filter_league": "Filtrovat podle ligové skupiny",
        "nav_dashboard": "Dashboard",
        "nav_simulator": "Sázková kalkulačka",
        "nav_schedule": "Kalendář zápasů",
        "nav_raw": "Průzkumník dat",
        "nav_docs": "Dokumentace",
        "schedule_title": "📅 Kalendář nadcházejících zápasů NHL",
        "schedule_desc": "Živý harmonogram nadcházejících ligových zápasů z oficiálního NHL API s možností okamžité predikce 1-klikem",
        "btn_simulate": "⚡ Simulovat zápas v kalkulačce",
        "err_data": "Data nebyla nalezena! Spusťte prosím nejprve skript `run.py`.",


        "info_run": "Pipeline spustíte příkazem `python run.py` v terminálu.",
        "help_total_teams": "Počet unikátních hokejových týmů obsažených v historických záznamech (df['team'].nunique()).",
        "help_total_seasons": "Počet odehraných ligových sezón pokrytých v datovém souboru (df['season'].nunique()).",
        "help_total_goals": "Celkový součet všech vstřelených gólů napříč všemi týmy a sezónami (df['scored_goals'].sum()).",
        "help_avg_win_pct": "Průměrné procento výher ze všech sezónních záznamů týmů (df['victory_percentage'].mean() * 100).",
        "help_win_prob": "Pravděpodobnost výhry vychází z poměru historické úspěšnosti obou týmů: P(A) = WinRate(A) / (WinRate(A) + WinRate(B)).",
        "help_odd": "Desetinný kurz vypočtený jako 1 / P(výhra) snížený o nastavenou marži bookmakera: Kurz = (1 / P) * (1 - marže).",
        "model_type": "Typ prediktivního modelu / vah",
        "model_baseline": "Historické statistiky (Baseline)",
        "model_form": "Klouzavé průměry (Forma z 3 sezón)",
        "model_logreg": "Logistická regrese (ML)",
        "model_rf": "Random Forest Classifier (Pokročilé ML)",
        "model_comp_title": "Porovnání predikcí všech ML modelů",
        "home_adv_label": "Výhoda domácího ledu (%)",
        "goalie_imp_label": "Vliv brankáře / absencí (%)",
        "bankroll_label": "Fiktivní rozpočet / Bankroll (Kč)",
        "tab_moneyline": "Moneyline (Výhra/Prohra)",
        "tab_overunder": "Over/Under (Počet gólů)",
        "tab_kelly_ev": "EV & Kellyho kalkulačka",
        "market_odd_label": "Kurz sázkové kanceláře (Tržní kurz)",
        "ev_label": "Očekávaná hodnota (EV %)",
        "kelly_stake_label": "Doporučená výše sázky (Half-Kelly)",
        "ou_threshold_label": "Hranice celkového počtu gólů",
        "exp_goals_total": "Očekávané góly celkem (Poisson λ)",
        "global_filters": "Globální filtry",
        "season_range_label": "Rozsah sezón",
        "corr_heatmap_title": "Korelační matice metrik (Heatmapa)",
        "goal_diff_label": "Brankový rozdíl (+/-)",
        "select_team_2": "Srovnat s druhým týmem (volitelné)",
        "none_option": "-- Žádný --",
        "heatmap_filter_label": "Filtrovat heatmapu podle týmu",
        "all_teams_option": "Celá liga (Všechny týmy)",
        "help_heatmap": "Globální korelace počítá vzájemné vztahy napříč všemi týmy ligy. Výběrem týmu zobrazíte specifickou korelační matici daného klubu.",
        "actual_teams_only": "Pouze současné týmy (Actual teams only)",
        "help_actual_teams": "Filtruje pouze aktivní týmy NHL a skryje historické/přejmenované franšízy (např. Atlanta Thrashers, Hartford Whalers, Mighty Ducks, Quebec Nordiques).",
        "help_bankroll": "Doporučená výše sázky spočítaná podle Half-Kellyho kritéria přizpůsobená zadanému bankrollu.",
        "ev_value_bet": "✅ **Value Bet!** Kurz sázkové kanceláře ({market_odd:.2f}) je vyšší než fér kurz modelu ({fair_odd:.2f}). Očekávaná ziskovost je +{ev_pct:.2f}%.",
        "ev_bad_bet": "⚠️ **Nevýhodná sázka!** Kurz sázkové kanceláře ({market_odd:.2f}) neobsahuje kladnou očekávanou hodnotu oproti modelu ({fair_odd:.2f})."
    },
    "EN": {
        "title": "Hockey Analytics Dashboard",
        "subtitle": "Premium betting insights, league classification, and historical trend analysis",
        "total_teams": "Total Teams",
        "total_seasons": "Total Seasons",
        "total_goals": "Total Goals",
        "avg_win_pct": "Avg. Win %",
        "visualizations": "League Performance Visualizations",
        "correlation": "Goals vs Victories Correlation",
        "goals_scored": "Goals Scored (GF)",
        "wins": "Victories (Wins)",
        "losses": "Losses",
        "victories_by_league": "Victories by League Category",
        "league_group": "League Group",
        "team_trend": "Team Trend Analysis",
        "select_team": "Select Team for Trend Analysis",
        "matches_count": "Matches count",
        "season": "Season",
        "model_properties": "Model Properties",
        "margin": "Bookmaker Margin (%)",
        "simulator_title": "Betting Odds Simulator",
        "simulator_desc": "Simulate matchup probabilities and view bookmaker odds incorporating margins",
        "home_team": "Home Team",
        "away_team": "Away Team",
        "warn_different": "Please choose two different teams to calculate odds.",
        "probabilities": "Matchup Probabilities",
        "win_probability": "Win Probability",
        "suggested_odds": "Suggested Odds",
        "decimal_odd_home": "Decimal Odd for {team} (Home)",
        "decimal_odd_away": "Decimal Odd for {team} (Away)",
        "raw_odd": "Raw: {odd:.2f}",
        "odd_label": "Odds: {odd:.2f}",
        "h2h_title": "Historical Stats Head-to-Head",
        "metric_col": "Metric",
        "total_wins_label": "Total Wins",
        "total_losses_label": "Total Losses",
        "goals_scored_label": "Goals Scored",
        "goals_conceded_label": "Goals Conceded",
        "raw_explorer": "Raw Data Explorer",
        "raw_explorer_desc": "Search, filter, and inspect the complete processed dataset",
        "search_team": "Search Team Name",
        "filter_league": "Filter by League Group",
        "nav_dashboard": "Dashboard",
        "nav_simulator": "Odds Calculator",
        "nav_schedule": "Match Schedule",
        "nav_raw": "Raw Explorer",
        "nav_docs": "Documentation",
        "schedule_title": "📅 Upcoming NHL Match Schedule",
        "schedule_desc": "Live schedule of upcoming games from the official NHL API with 1-click instant prediction simulation",
        "btn_simulate": "⚡ Simulate Match in Calculator",
        "err_data": "Data was not found! Please run the pipeline script `run.py` first to collect and process data.",
        "info_run": "You can run the data pipeline by executing `python run.py` in the terminal.",
        "help_total_teams": "Number of unique hockey teams in historical records (df['team'].nunique()).",
        "help_total_seasons": "Number of league seasons covered in the dataset (df['season'].nunique()).",
        "help_total_goals": "Total sum of goals scored across all teams and seasons (df['scored_goals'].sum()).",
        "help_avg_win_pct": "Average win percentage across all seasonal team records (df['victory_percentage'].mean() * 100).",
        "help_win_prob": "Win probability based on relative win rates: P(A) = WinRate(A) / (WinRate(A) + WinRate(B)).",
        "help_odd": "Decimal odds calculated as 1 / P(win) minus bookmaker margin: Odd = (1 / P) * (1 - margin).",
        "model_type": "Predictive Model / Weighting Type",
        "model_baseline": "Historical Baseline",
        "model_form": "Rolling Form (Last 3 Seasons)",
        "model_logreg": "Logistic Regression (ML)",
        "model_rf": "Random Forest Classifier (Advanced ML)",
        "model_comp_title": "Predictive ML Models Comparison",
        "home_adv_label": "Home Ice Advantage (%)",
        "goalie_imp_label": "Goalie / Absence Impact (%)",
        "bankroll_label": "Virtual Bankroll ($)",
        "tab_moneyline": "Moneyline (Win/Loss)",
        "tab_overunder": "Over/Under (Total Goals)",
        "tab_kelly_ev": "EV & Kelly Calculator",
        "market_odd_label": "Bookmaker Market Odds",
        "ev_label": "Expected Value (EV %)",
        "kelly_stake_label": "Recommended Stake (Half-Kelly)",
        "ou_threshold_label": "Total Goal Threshold",
        "exp_goals_total": "Expected Total Goals (Poisson λ)",
        "global_filters": "Global Filters",
        "season_range_label": "Season Range",
        "corr_heatmap_title": "Metrics Correlation Heatmap",
        "goal_diff_label": "Goal Difference (+/-)",
        "select_team_2": "Compare with 2nd Team (Optional)",
        "none_option": "-- None --",
        "heatmap_filter_label": "Filter heatmap by team",
        "all_teams_option": "Entire League (All Teams)",
        "help_heatmap": "Global correlation evaluates relationships across all league teams. Select a specific team to inspect that franchise's historical correlation matrix.",
        "actual_teams_only": "Actual teams only",
        "help_actual_teams": "Filters only current active NHL franchises and excludes historical/defunct/relocated names (e.g. Atlanta Thrashers, Hartford Whalers, Mighty Ducks, Quebec Nordiques).",
        "help_bankroll": "Recommended stake calculated using Half-Kelly criterion adjusted to the given bankroll.",
        "ev_value_bet": "✅ **Value Bet!** Market odds ({market_odd:.2f}) are higher than model fair odds ({fair_odd:.2f}). Expected ROI is +{ev_pct:.2f}%.",
        "ev_bad_bet": "⚠️ **Negative EV Bet!** Market odds ({market_odd:.2f}) do not offer positive expected value compared to model fair odds ({fair_odd:.2f})."
    }
}








# Helper to load dataset
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "hockey_teams.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path, sep=';')
    return None

df = load_data()

# Helper to load Coders Lab logo icon
def get_cl_logo_b64():
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_cl.png")
    if os.path.exists(logo_path):
        import base64
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

cl_b64 = get_cl_logo_b64()

# Coderslab Branding with Clickable CL Logo Link
st.sidebar.markdown(f"""
<div style="font-family: 'Inter', 'Segoe UI', sans-serif; text-align: center; margin-bottom: 5px; padding: 5px 0;">
    <a href="https://coderslab.cz/cz/kurzy/data-analyst" target="_blank" title="Coders Lab - Data Analyst Course" style="text-decoration: none; display: inline-block; margin-bottom: 8px;">
        <img src="data:image/png;base64,{cl_b64}" style="height: 52px; border-radius: 8px; box-shadow: 0 4px 15px rgba(253, 184, 19, 0.4);" alt="Coders Lab Data Analyst Course">
    </a>
    <div style="font-size: 2.2rem; font-weight: 700; line-height: 1.1; margin-bottom: 8px;">
        <span class="logo-c">Coders</span><span class="logo-l" style="margin-left: 2px;">Lab</span>
    </div>
    <div style="display: flex; align-items: center; justify-content: center; width: 100%;">
        <div class="logo-line" style="height: 1px; flex-grow: 1;"></div>
        <div style="font-size: 0.65rem; font-weight: 600; letter-spacing: 3px; padding: 0 8px; white-space: nowrap; text-transform: uppercase;">
            IT Academy
        </div>
        <div class="logo-line" style="height: 1px; flex-grow: 1;"></div>
    </div>
</div>
<div style="font-size: 0.8rem; color: #8892B0; text-align: center; margin-bottom: 10px; font-family: sans-serif; margin-top: 10px;">
    <a href="https://coderslab.cz/cz/kurzy/data-analyst" target="_blank" style="color: inherit; text-decoration: none;">
        Data Analyst Course<br><b class="logo-c">Vít Otáhal</b>
    </a>
</div>
""", unsafe_allow_html=True)



# Auto-detect client browser language and restore from URL query parameters / session state
if 'lang' not in st.session_state:
    query_lang = st.query_params.get("lang", None)
    if query_lang in ["EN", "CZ"]:
        st.session_state['lang'] = query_lang
    else:
        try:
            accept_lang = st.context.headers.get("Accept-Language", "").lower()
            if "cs" in accept_lang or "sk" in accept_lang:
                st.session_state['lang'] = "CZ"
            else:
                st.session_state['lang'] = "EN"
        except Exception:
            st.session_state['lang'] = "CZ"

# Symmetrical Controls Row (Language flags and Theme toggle)
c1, c2 = st.sidebar.columns(2)
with c1:
    lang_selected = st.selectbox(
        "Language", ["English", "Čeština"], 
        index=0 if st.session_state.get('lang', 'CZ') == 'EN' else 1,
        label_visibility="collapsed"
    )
    lang = "EN" if lang_selected == "English" else "CZ"
    st.session_state['lang'] = lang
    st.query_params["lang"] = lang
    labels = t[lang]

with c2:
    theme_selected = st.selectbox(
        "Theme", ["Light", "Dark"] if lang == "EN" else ["Světlý", "Tmavý"], 
        index=1 if st.session_state.get('theme', 'dark') == 'dark' else 0,
        label_visibility="collapsed"
    )
    theme = "dark" if "Dark" in theme_selected or "Tmavý" in theme_selected else "light"
    st.session_state['theme'] = theme

plotly_template = "plotly_dark" if theme == "dark" else "plotly_white"

plotly_bg = "#0E1117" if theme == "dark" else "#FFFFFF"
plotly_font_color = "#E0E6ED" if theme == "dark" else "#31333F"

# Inject Theme Override CSS

if theme == "dark":
    st.markdown("""
    <style>
        .stApp {
            background-color: #0E1117 !important;
            color: #E0E6ED !important;
        }
        :root {
            --background-color: #0E1117 !important;
            --secondary-background-color: #1F2635 !important;
            --text-color: #E0E6ED !important;
        }
        /* Main App Body High-Contrast Text Rules for Dark Mode */
        .stApp, .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
            color: #E0E6ED !important;
        }
        /* Style st.metric labels & values in Dark Mode */
        div[data-testid="stMetricLabel"] *, div[data-testid="stMetricLabel"] p, div[data-testid="stMetricLabel"] span {
            color: #8892B0 !important;
        }
        div[data-testid="stMetricValue"] *, div[data-testid="stMetricValue"] {
            color: #FFFFFF !important;
        }
        /* Style st.table (Historical Head-to-Head Stats table) in Dark Mode */
        div[data-testid="stTable"] table {
            background-color: #1F2635 !important;
            border: 1px solid #2D3748 !important;
            border-radius: 8px !important;
        }
        div[data-testid="stTable"] th {
            background-color: #161B25 !important;
            color: #FFFFFF !important;
            font-weight: bold !important;
            border-bottom: 2px solid #2D3748 !important;
        }
        div[data-testid="stTable"] td {
            background-color: #1F2635 !important;
            color: #E0E6ED !important;
            border-bottom: 1px solid #2D3748 !important;
        }
        /* Fullscreen, Plotly and Modal Containers styling for Dark Mode */
        :fullscreen, :-webkit-full-screen, :-moz-full-screen, :-ms-fullscreen,
        div[data-testid="stFullScreenFrame"], 
        div[data-modal-container="true"],
        div[data-testid="stDialog"],
        .js-plotly-plot, .plot-container, .plotly, .plotly-graph-div {
            background-color: #0E1117 !important;
            background: #0E1117 !important;
            color: #E0E6ED !important;
        }
        /* Force Plotly SVG background rectangle to dark in Dark Mode */
        svg.main-svg rect.bg {
            fill: #0E1117 !important;
        }
        /* Force Plotly SVG text elements to light color in Dark Mode */
        svg.main-svg .g-gtitle text, 
        svg.main-svg .g-xtitle text, 
        svg.main-svg .g-ytitle text, 
        svg.main-svg .xtick text, 
        svg.main-svg .ytick text, 
        svg.main-svg .legendtext {
            fill: #E0E6ED !important;
        }
        /* Sidebar styling for Dark Mode */
        section[data-testid="stSidebar"] {
            background-color: #161B25 !important;
            color: #E0E6ED !important;
        }
        /* Ensure ALL text inside sidebar is high-contrast light color in Dark Mode */
        section[data-testid="stSidebar"] span, 
        section[data-testid="stSidebar"] label, 
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] div {
            color: #E0E6ED !important;
        }
        /* Style unopened selectbox and input controls in Dark Mode */
        div[data-baseweb="select"] > div, 
        div[data-baseweb="input"],
        div[data-baseweb="input"] *,
        div[data-baseweb="base-input"],
        div[data-baseweb="base-input"] *,
        input[data-testid="stTextInput"] {
            background-color: #1F2635 !important;
            color: #E0E6ED !important;
            border-color: #2D3748 !important;
        }
        div[data-baseweb="select"] * {
            color: #E0E6ED !important;
            fill: #E0E6ED !important;
        }
        /* Style DataFrame container and Canvas in Dark Mode */
        div[data-testid="stDataFrame"], 
        div[data-testid="stDataFrame"] > div, 
        div[data-testid="stDataFrame"] [data-testid="stTable"] {
            background-color: #1F2635 !important;
            color: #E0E6ED !important;
            border: 1px solid #2D3748 !important;
        }
        div[data-testid="stDataFrame"] canvas {
            filter: invert(0.9) hue-rotate(180deg) !important;
        }
        /* Style the selectbox dropdown popover in Dark Mode */
        div[data-baseweb="popover"], div[role="listbox"], div[role="option"] {
            background-color: #1F2635 !important;
            color: #E0E6ED !important;
        }
        div[role="option"]:hover, div[data-baseweb="popover"] li:hover {
            background-color: #2D3748 !important;
        }
        /* Protect brand colors from being overridden */
        .logo-c {
            color: #E0E6ED !important;
        }
        .logo-l {
            color: #FDB813 !important;
        }
        .logo-line {
            background-color: #FDB813 !important;
        }
    </style>
    """, unsafe_allow_html=True)


else:
    st.markdown("""
    <style>
        .stApp {
            background-color: #FFFFFF !important;
            color: #31333F !important;
        }
        :root {
            --background-color: #FFFFFF !important;
            --secondary-background-color: #F0F2F6 !important;
            --text-color: #31333F !important;
        }
        /* Main App Body High-Contrast Text Rules for Light Mode */
        .stApp, .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
            color: #31333F !important;
        }
        /* Style st.metric labels & values in Light Mode */
        div[data-testid="stMetricLabel"] *, div[data-testid="stMetricLabel"] p, div[data-testid="stMetricLabel"] span {
            color: #555555 !important;
        }
        div[data-testid="stMetricValue"] *, div[data-testid="stMetricValue"] {
            color: #111111 !important;
        }
        /* Style st.table (Historical Head-to-Head Stats table) in Light Mode */
        div[data-testid="stTable"] table {
            background-color: #F0F2F6 !important;
            border: 1px solid rgba(0,0,0,0.1) !important;
            border-radius: 8px !important;
        }
        div[data-testid="stTable"] th {
            background-color: #E2E8F0 !important;
            color: #111111 !important;
            font-weight: bold !important;
            border-bottom: 2px solid rgba(0,0,0,0.1) !important;
        }
        div[data-testid="stTable"] td {
            background-color: #F0F2F6 !important;
            color: #31333F !important;
            border-bottom: 1px solid rgba(0,0,0,0.05) !important;
        }
        /* Fullscreen, Plotly and Modal Containers styling for Light Mode */
        :fullscreen, :-webkit-full-screen, :-moz-full-screen, :-ms-fullscreen,
        div[data-testid="stFullScreenFrame"], 
        div[data-modal-container="true"],
        div[data-testid="stDialog"],
        .js-plotly-plot, .plot-container, .plotly, .plotly-graph-div {
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            color: #31333F !important;
        }
        /* Force Plotly SVG background rectangle to light in Light Mode */
        svg.main-svg rect.bg {
            fill: #FFFFFF !important;
        }
        /* Force Plotly SVG text elements to dark color in Light Mode */
        svg.main-svg .g-gtitle text, 
        svg.main-svg .g-xtitle text, 
        svg.main-svg .g-ytitle text, 
        svg.main-svg .xtick text, 
        svg.main-svg .ytick text, 
        svg.main-svg .legendtext {
            fill: #31333F !important;
        }
        /* Sidebar styling for Light Mode */
        section[data-testid="stSidebar"] {
            background-color: #F0F2F6 !important;
            color: #31333F !important;
        }
        /* Ensure ALL text inside sidebar is high-contrast dark color in Light Mode */
        section[data-testid="stSidebar"] span, 
        section[data-testid="stSidebar"] label, 
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] div {
            color: #31333F !important;
        }
        /* Style unopened selectbox and input controls in Light Mode */
        div[data-baseweb="select"] > div, 
        div[data-baseweb="input"],
        div[data-baseweb="input"] *,
        div[data-baseweb="base-input"],
        div[data-baseweb="base-input"] *,
        input[data-testid="stTextInput"] {
            background-color: #F0F2F6 !important;
            color: #31333F !important;
            border-color: rgba(0, 0, 0, 0.1) !important;
        }
        div[data-baseweb="select"] * {
            color: #31333F !important;
            fill: #31333F !important;
        }
        /* Style DataFrame container and Canvas in Light Mode */
        div[data-testid="stDataFrame"], 
        div[data-testid="stDataFrame"] > div, 
        div[data-testid="stDataFrame"] [data-testid="stTable"] {
            background-color: #F0F2F6 !important;
            color: #31333F !important;
            border: 1px solid rgba(0, 0, 0, 0.1) !important;
        }
        div[data-testid="stDataFrame"] canvas {
            filter: none !important;
        }
        /* Style the selectbox dropdown popover in Light Mode */
        div[data-baseweb="popover"], div[role="listbox"], div[role="option"] {
            background-color: #F0F2F6 !important;
            color: #31333F !important;
        }
        div[role="option"]:hover, div[data-baseweb="popover"] li:hover {
            background-color: #E2E8F0 !important;
        }
        section[data-testid="stSidebar"] hr {
            border-color: rgba(0, 0, 0, 0.1) !important;
        }
        /* Protect brand colors from being overridden */
        .logo-c {
            color: #31333F !important;
        }
        .logo-l {
            color: #FDB813 !important;
        }
        .logo-line {
            background-color: #FDB813 !important;
        }
    </style>
    """, unsafe_allow_html=True)











if df is None:
    st.title("🏒 Overtime Analytics")
    st.error(labels["err_data"])
    st.info(labels["info_run"])
else:
    # Sidebar navigation
    with st.sidebar:
        st.markdown("---")
        
        # Check if a pending navigation redirect was requested
        if "pending_nav" in st.session_state:
            st.session_state["main_navigation_radio"] = st.session_state.pop("pending_nav")
            
        nav_options = [labels["nav_dashboard"], labels["nav_simulator"], labels["nav_schedule"], labels["nav_raw"], labels["nav_docs"]]
        
        menu = st.radio(
            "Navigation" if lang == "EN" else "Navigace",
            nav_options,
            key="main_navigation_radio"
        )
        st.session_state["nav_choice"] = menu



        
        st.markdown("---")
        st.markdown(f"### {labels['global_filters']}")
        
        only_actual_teams = st.checkbox(labels["actual_teams_only"], value=False, help=labels["help_actual_teams"])
        
        min_s = int(df['season'].min())
        max_s = int(df['season'].max())
        selected_seasons = st.slider(
            labels["season_range_label"],
            min_value=min_s, max_value=max_s,
            value=(min_s, max_s)
        )
        
        # Apply global filters
        if only_actual_teams:
            defunct_teams = {"Atlanta Thrashers", "Hartford Whalers", "Mighty Ducks of Anaheim", "Minnesota North Stars", "Phoenix Coyotes", "Quebec Nordiques"}
            df = df[~df['team'].isin(defunct_teams)].copy()
            
        df = df[(df['season'] >= selected_seasons[0]) & (df['season'] <= selected_seasons[1])].copy()


        st.markdown("---")
        st.markdown(f"### {labels['model_properties']}")
        margin = st.slider(labels["margin"], min_value=0.0, max_value=15.0, value=5.0, step=0.5) / 100.0
        home_adv = st.slider(labels["home_adv_label"], min_value=0.0, max_value=15.0, value=5.0, step=0.5)
        goalie_imp = st.slider(labels["goalie_imp_label"], min_value=-10.0, max_value=10.0, value=0.0, step=0.5)
        bankroll = st.number_input(labels["bankroll_label"], min_value=100.0, max_value=1000000.0, value=10000.0, step=500.0)
        
        st.markdown("---")
        st.caption("Powered by Streamlit & BeautifulSoup")



        
    if menu == labels["nav_dashboard"]:
        # Header
        st.markdown(f"<div class='main-title'>{labels['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtitle'>{labels['subtitle']}</div>", unsafe_allow_html=True)
        
        # Core Metrics
        total_teams = df['team'].nunique()
        total_seasons = df['season'].nunique()
        total_goals = df['scored_goals'].sum()
        avg_win_pct = df['victory_percentage'].mean() * 100
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">{labels['total_teams']} <span class="help-icon" title="{labels['help_total_teams']}">?</span></div>
                <div class="metric-val">{total_teams}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">{labels['total_seasons']} <span class="help-icon" title="{labels['help_total_seasons']}">?</span></div>
                <div class="metric-val">{total_seasons}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">{labels['total_goals']} <span class="help-icon" title="{labels['help_total_goals']}">?</span></div>
                <div class="metric-val">{total_goals:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">{labels['avg_win_pct']} <span class="help-icon" title="{labels['help_avg_win_pct']}">?</span></div>
                <div class="metric-val">{avg_win_pct:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

            
        st.markdown(f"### {labels['visualizations']}")
        
        col_chart1, col_chart2 = st.columns(2)
        
        plotly_template = "plotly_dark" if theme == "dark" else "plotly_white"
        plotly_bg = "#0E1117" if theme == "dark" else "#FFFFFF"
        plotly_font_color = "#E0E6ED" if theme == "dark" else "#31333F"

        with col_chart1:
            st.markdown(f"#### {labels['correlation']}")
            fig = px.scatter(
                df, x='scored_goals', y='victories', color='league',
                hover_data=['team', 'season'],
                labels={'scored_goals': labels['goals_scored'], 'victories': labels['wins']},
                color_discrete_sequence=px.colors.qualitative.Pastel,
                template=plotly_template
            )
            fig.update_layout(
                paper_bgcolor=plotly_bg,
                plot_bgcolor=plotly_bg,
                font=dict(color=plotly_font_color)
            )
            st.plotly_chart(fig, width="stretch")

            
        with col_chart2:
            st.markdown(f"#### {labels['victories_by_league']}")
            fig2 = px.box(
                df, x='league', y='victories', points='all',
                color='league',
                labels={'league': labels['league_group'], 'victories': labels['wins']},
                color_discrete_sequence=px.colors.qualitative.Pastel,
                template=plotly_template
            )
            fig2.update_layout(
                paper_bgcolor=plotly_bg,
                plot_bgcolor=plotly_bg,
                font=dict(color=plotly_font_color)
            )
            st.plotly_chart(fig2, width="stretch")

        st.markdown("---")
        st.markdown(f"### {labels['corr_heatmap_title']}")
        
        heatmap_team_filter = st.selectbox(
            labels["heatmap_filter_label"],
            [labels["all_teams_option"]] + sorted(df['team'].unique()),
            help=labels["help_heatmap"]
        )
        
        if heatmap_team_filter != labels["all_teams_option"]:
            df_heatmap_src = df[df['team'] == heatmap_team_filter]
        else:
            df_heatmap_src = df
            
        corr_cols = ['scored_goals', 'received_goals', 'victories', 'defeats', 'goal_difference', 'victory_percentage']
        corr_labels = {
            'scored_goals': labels['goals_scored_label'],
            'received_goals': labels['goals_conceded_label'],
            'victories': labels['total_wins_label'],
            'defeats': labels['total_losses_label'],
            'goal_difference': labels['goal_diff_label'],
            'victory_percentage': labels['avg_win_pct']
        }
        
        df_corr = df_heatmap_src[corr_cols].rename(columns=corr_labels).corr().round(2)
        
        fig_heatmap = px.imshow(
            df_corr, text_auto=True, color_continuous_scale='RdBu_r', aspect="auto", template=plotly_template
        )
        fig_heatmap.update_traces(textfont=dict(size=15, color='#FFFFFF', family="sans-serif"))
        fig_heatmap.update_layout(
            paper_bgcolor=plotly_bg,
            plot_bgcolor=plotly_bg,
            font=dict(color=plotly_font_color, size=13),
            xaxis=dict(tickfont=dict(size=13, color=plotly_font_color)),
            yaxis=dict(tickfont=dict(size=13, color=plotly_font_color))
        )
        st.plotly_chart(fig_heatmap, width="stretch")


            
        st.markdown("---")
        st.markdown(f"### {labels['team_trend']}")
        col_t1, col_t2 = st.columns(2)
        sorted_teams = sorted(df['team'].unique())
        
        with col_t1:
            selected_team_1 = st.selectbox(labels["select_team"], sorted_teams, index=0)
        with col_t2:
            selected_team_2 = st.selectbox(labels["select_team_2"], [labels["none_option"]] + sorted_teams, index=0)
            
        team_df_1 = df[df['team'] == selected_team_1].sort_values('season')
        
        # Team Logos Display Header
        col_logo1, col_logo2 = st.columns(2)
        with col_logo1:
            st.markdown(f"<div style='text-align: center;'><img src='{get_team_logo(selected_team_1)}' style='height: 70px; margin-bottom: 0.5rem;'><h4 style='color: #FF4B4B;'>{selected_team_1}</h4></div>", unsafe_allow_html=True)
        with col_logo2:
            if selected_team_2 != labels["none_option"]:
                st.markdown(f"<div style='text-align: center;'><img src='{get_team_logo(selected_team_2)}' style='height: 70px; margin-bottom: 0.5rem;'><h4 style='color: #FDB813;'>{selected_team_2}</h4></div>", unsafe_allow_html=True)

        
        fig3 = go.Figure(layout=dict(template=plotly_template))
        fig3.add_trace(go.Scatter(
            x=team_df_1['season'], y=team_df_1['victories'],
            name=f"{selected_team_1} ({labels['wins']})",
            line=dict(color='#FF4B4B', width=3)
        ))
        fig3.add_trace(go.Scatter(
            x=team_df_1['season'], y=team_df_1['defeats'],
            name=f"{selected_team_1} ({labels['losses']})",
            line=dict(color='#8892B0', width=2, dash='dot')
        ))
        
        if selected_team_2 != labels["none_option"]:
            team_df_2 = df[df['team'] == selected_team_2].sort_values('season')
            fig3.add_trace(go.Scatter(
                x=team_df_2['season'], y=team_df_2['victories'],
                name=f"{selected_team_2} ({labels['wins']})",
                line=dict(color='#FDB813', width=3)
            ))
            fig3.add_trace(go.Scatter(
                x=team_df_2['season'], y=team_df_2['defeats'],
                name=f"{selected_team_2} ({labels['losses']})",
                line=dict(color='#4A5568', width=2, dash='dot')
            ))
            
        fig3.update_layout(
            paper_bgcolor=plotly_bg,
            plot_bgcolor=plotly_bg,
            font=dict(color=plotly_font_color),
            xaxis=dict(
                title=labels['season'],
                dtick=1,
                type='linear'
            )
        )
        st.plotly_chart(fig3, width="stretch")




    elif menu == labels["nav_simulator"]:
        st.markdown(f"<div class='main-title'>{labels['simulator_title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtitle'>{labels['simulator_desc']}</div>", unsafe_allow_html=True)
        
        teams = sorted(df['team'].unique())
        
        # Initialize default team selections if not set
        if "team_a_select" not in st.session_state or st.session_state["team_a_select"] not in teams:
            st.session_state["team_a_select"] = teams[0] if teams else ""
        if "team_b_select" not in st.session_state or st.session_state["team_b_select"] not in teams:
            st.session_state["team_b_select"] = teams[min(1, len(teams)-1)] if teams else ""
        
        col_team1, col_team2, col_model = st.columns([1, 1, 1])
        
        with col_team1:
            team_a = st.selectbox(labels["home_team"], teams, key="team_a_select")

        with col_team2:
            team_b = st.selectbox(labels["away_team"], teams, key="team_b_select")
        
        with col_model:
            model_selected = st.selectbox(
                labels["model_type"],
                [labels["model_baseline"], labels["model_form"], labels["model_logreg"], labels["model_rf"]],
                index=3
            )

            
        if team_a == team_b:
            st.warning(labels["warn_different"])
        else:
            # Predict using Machine Learning module
            ml_predictor = get_ml_predictor(df)
            all_preds = ml_predictor.predict_matchup(df, team_a, team_b, home_advantage_pct=home_adv, goalie_impact_pct=goalie_imp)

            
            # Select probabilities based on user choice
            if model_selected == labels["model_form"]:
                prob_a, prob_b = all_preds["form"]
            elif model_selected == labels["model_logreg"]:
                prob_a, prob_b = all_preds["logreg"]
            elif model_selected == labels["model_rf"]:
                prob_a, prob_b = all_preds["rf"]
            else:
                prob_a, prob_b = all_preds["baseline"]
            
            # Ensure non-zero probabilities
            prob_a = max(0.01, min(0.99, prob_a))
            prob_b = max(0.01, min(0.99, prob_b))
            
            # Calculate raw odds
            raw_odd_a = 1.0 / prob_a
            raw_odd_b = 1.0 / prob_b
            
            # Adjust odds with margin
            adj_odd_a = max(1.01, raw_odd_a * (1.0 - margin))
            adj_odd_b = max(1.01, raw_odd_b * (1.0 - margin))

            
            tab_m, tab_ou, tab_ev = st.tabs([labels["tab_moneyline"], labels["tab_overunder"], labels["tab_kelly_ev"]])
            
            with tab_m:
                # Display Simulation Details in a Beautiful Card with Team Logos
                logo_a = get_team_logo(team_a)
                logo_b = get_team_logo(team_b)
                
                st.markdown(f"""<div class="calc-container">
<h3 style="color: var(--text-color); text-align: center; margin-bottom: 2rem;">{labels['probabilities']}</h3>
<div style="display: flex; justify-content: space-around; align-items: center; margin-bottom: 2rem;">
<div style="text-align: center;">
<img src="{logo_a}" style="height: 80px; margin-bottom: 0.5rem;" alt="{team_a}">
<h4 style="color: #FF4B4B; margin: 0;">{team_a}</h4>
<div style="font-size: 2.5rem; font-weight: 800; color: var(--text-color); margin: 0.5rem 0;">{prob_a * 100:.1f}%</div>
<p style="color: #8892B0; margin: 0;">{labels['win_probability']}</p>
</div>
<div style="font-size: 2.2rem; font-weight: 800; color: #FDB813; text-shadow: 0 0 10px rgba(253, 184, 19, 0.3);">VS</div>
<div style="text-align: center;">
<img src="{logo_b}" style="height: 80px; margin-bottom: 0.5rem;" alt="{team_b}">
<h4 style="color: #38BDF8; margin: 0;">{team_b}</h4>
<div style="font-size: 2.5rem; font-weight: 800; color: var(--text-color); margin: 0.5rem 0;">{prob_b * 100:.1f}%</div>
<p style="color: #8892B0; margin: 0;">{labels['win_probability']}</p>
</div>
</div>
</div>""", unsafe_allow_html=True)


                # Show Odds & Recommended Stake Comparison
                st.markdown(f"### {labels['suggested_odds']}")
                
                kelly_m = HockeyPredictorML.calculate_kelly_and_ev(prob_a, adj_odd_a, bankroll=bankroll)
                currency_unit = "Kč" if lang == "CZ" else "$"
                
                col_o1, col_o2, col_o3 = st.columns(3)
                with col_o1:
                    st.metric(
                        label=labels["decimal_odd_home"].format(team=team_a),
                        value=f"{adj_odd_a:.2f}",
                        delta=labels["raw_odd"].format(odd=raw_odd_a),
                        help=labels["help_odd"]
                    )
                with col_o2:
                    st.metric(
                        label=labels["decimal_odd_away"].format(team=team_b),
                        value=f"{adj_odd_b:.2f}",
                        delta=labels["raw_odd"].format(odd=raw_odd_b),
                        help=labels["help_odd"]
                    )
                with col_o3:
                    st.metric(
                        label=labels["kelly_stake_label"],
                        value=f"{kelly_m['recommended_stake']:,.0f} {currency_unit}",
                        delta=f"{kelly_m['kelly_pct']:.1f} % (EV {kelly_m['ev_pct']:+.1f}%)" if kelly_m['ev_pct'] > 0 else "0 % (EV ≤ 0%)",
                        help=labels["help_bankroll"]
                    )


                # Model Comparison Chart
                st.markdown("---")
                st.markdown(f"### {labels['model_comp_title']}")
                
                comp_models = [labels["model_baseline"], labels["model_form"], labels["model_logreg"], labels["model_rf"]]
                prob_a_list = [all_preds["baseline"][0]*100, all_preds["form"][0]*100, all_preds["logreg"][0]*100, all_preds["rf"][0]*100]
                prob_b_list = [all_preds["baseline"][1]*100, all_preds["form"][1]*100, all_preds["logreg"][1]*100, all_preds["rf"][1]*100]
                
                hover_label_prob = "Pravděpodobnost" if lang == "CZ" else "Probability"
                
                fig_comp = go.Figure()
                fig_comp.add_trace(go.Bar(
                    x=comp_models, y=prob_a_list, name=team_a, marker_color='#FF4B4B', 
                    text=[f"<b>{p:.1f}%</b>" for p in prob_a_list], textposition='auto',
                    textfont=dict(size=15, color='#FFFFFF'),
                    hovertemplate=f"<b style='font-size:1.1em;'>{team_a}</b><br>Model: %{{x}}<br>{hover_label_prob}: <b>%{{y:.1f}}%</b><extra></extra>"
                ))
                fig_comp.add_trace(go.Bar(
                    x=comp_models, y=prob_b_list, name=team_b, marker_color='#38BDF8', 
                    text=[f"<b>{p:.1f}%</b>" for p in prob_b_list], textposition='auto',
                    textfont=dict(size=15, color='#FFFFFF'),
                    hovertemplate=f"<b style='font-size:1.1em;'>{team_b}</b><br>Model: %{{x}}<br>{hover_label_prob}: <b>%{{y:.1f}}%</b><extra></extra>"
                ))


                fig_comp.update_layout(
                    barmode='group',
                    paper_bgcolor=plotly_bg,
                    plot_bgcolor=plotly_bg,
                    font=dict(color=plotly_font_color, size=13),
                    xaxis=dict(tickfont=dict(size=13, color=plotly_font_color)),
                    yaxis=dict(title="Pravděpodobnost výhry (%)" if lang == "CZ" else "Win Probability (%)", range=[0, 105], tickfont=dict(size=13, color=plotly_font_color))
                )
                fig_comp.update_traces(textfont=dict(size=15, color='#FFFFFF'))
                st.plotly_chart(fig_comp, width="stretch")


                # Historical Head-to-Head Stats Comparison Table
                st.markdown(f"### {labels['h2h_title']}")
                stats_a = df[df['team'] == team_a].agg({
                    'victories': 'sum', 'defeats': 'sum', 'scored_goals': 'sum', 'received_goals': 'sum'
                })
                stats_b = df[df['team'] == team_b].agg({
                    'victories': 'sum', 'defeats': 'sum', 'scored_goals': 'sum', 'received_goals': 'sum'
                })
                comparison_data = {
                    labels['metric_col']: [
                        labels['total_wins_label'],
                        labels['total_losses_label'],
                        labels['goals_scored_label'],
                        labels['goals_conceded_label']
                    ],
                    team_a: [stats_a['victories'], stats_a['defeats'], stats_a['scored_goals'], stats_a['received_goals']],
                    team_b: [stats_b['victories'], stats_b['defeats'], stats_b['scored_goals'], stats_b['received_goals']]
                }
                comp_df = pd.DataFrame(comparison_data)
                st.table(comp_df.set_index(labels['metric_col']))

            with tab_ou:
                st.markdown(f"### {labels['tab_overunder']}")
                ou_threshold = st.selectbox(labels["ou_threshold_label"], [4.5, 5.5, 6.5], index=1)
                
                ou_res = ml_predictor.predict_over_under(df, team_a, team_b, threshold=ou_threshold)
                
                st.info(f"{labels['exp_goals_total']}: **{ou_res['lambda_total']:.2f}** ({team_a}: {ou_res['lambda_a']:.2f}, {team_b}: {ou_res['lambda_b']:.2f})")
                
                col_ou1, col_ou2 = st.columns(2)
                with col_ou1:
                    st.metric(
                        label=f"Under {ou_threshold}",
                        value=f"{ou_res['prob_under']*100:.1f}%",
                        delta=labels["odd_label"].format(odd=ou_res['odd_under'])
                    )
                with col_ou2:
                    st.metric(
                        label=f"Over {ou_threshold}",
                        value=f"{ou_res['prob_over']*100:.1f}%",
                        delta=labels["odd_label"].format(odd=ou_res['odd_over'])
                    )

            with tab_ev:
                st.markdown(f"### {labels['tab_kelly_ev']}")
                col_ev1, col_ev2 = st.columns(2)
                with col_ev1:
                    market_odd_input = st.number_input(
                        labels["market_odd_label"],
                        min_value=1.01, max_value=50.0, value=float(f"{adj_odd_a:.2f}"), step=0.05
                    )
                with col_ev2:
                    st.markdown(f"**Modelová pravděpodobnost výhry ({team_a}):** {prob_a * 100:.1f}%" if lang == "CZ" else f"**Model Win Probability ({team_a}):** {prob_a * 100:.1f}%")
                    st.markdown(f"**Fér kurz modelu:** {1.0/prob_a:.2f}" if lang == "CZ" else f"**Model Fair Odds:** {1.0/prob_a:.2f}")

                kelly_res = HockeyPredictorML.calculate_kelly_and_ev(prob_a, market_odd_input, bankroll=bankroll)
                
                col_k1, col_k2 = st.columns(2)
                with col_k1:
                    st.metric(labels["ev_label"], f"{kelly_res['ev_pct']:+.2f}%")
                with col_k2:
                    currency_unit = "Kč" if lang == "CZ" else "$"
                    st.metric(labels["kelly_stake_label"], f"{kelly_res['recommended_stake']:,.0f} {currency_unit} ({kelly_res['kelly_pct']:.1f} %)")
                
                if kelly_res['ev_pct'] > 0:
                    st.success(labels["ev_value_bet"].format(market_odd=market_odd_input, fair_odd=1.0/prob_a, ev_pct=kelly_res['ev_pct']))
                else:
                    st.warning(labels["ev_bad_bet"].format(market_odd=market_odd_input, fair_odd=1.0/prob_a))

    elif menu == labels["nav_schedule"]:
        st.markdown(f"<div class='main-title'>{labels['schedule_title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtitle'>{labels['schedule_desc']}</div>", unsafe_allow_html=True)
        
        matches = get_upcoming_matches(max_matches=12)
        
        if not matches:
            st.info("Žádné nadcházející zápasy nebyly nalezeny." if lang == "CZ" else "No upcoming matches found.")
        else:
            for idx, m in enumerate(matches):
                h_name = m["home_team"]
                a_name = m["away_team"]
                h_logo = get_team_logo(h_name)
                a_logo = get_team_logo(a_name)
                
                with st.container():
                    col_m1, col_m2, col_m3, col_m4 = st.columns([2, 0.8, 2, 1.5], vertical_alignment="center")
                    
                    with col_m1:
                        st.markdown(f"""
                        <div style="display: flex; align-items: center; justify-content: flex-end; text-align: right; gap: 12px;">
                            <div>
                                <div style="font-weight: 700; font-size: 1.1rem; color: #FF4B4B;">{h_name}</div>
                                <div style="font-size: 0.8rem; color: #8892B0;">Home</div>
                            </div>
                            <img src="{h_logo}" style="height: 48px;" alt="{h_name}">
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with col_m2:
                        st.markdown(f"""
                        <div style="text-align: center; font-weight: 800; font-size: 1.4rem; color: #FDB813; display: flex; align-items: center; justify-content: center; height: 100%;">
                            VS
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with col_m3:
                        st.markdown(f"""
                        <div style="display: flex; align-items: center; justify-content: flex-start; text-align: left; gap: 12px;">
                            <img src="{a_logo}" style="height: 48px;" alt="{a_name}">
                            <div>
                                <div style="font-weight: 700; font-size: 1.1rem; color: #38BDF8;">{a_name}</div>
                                <div style="font-size: 0.8rem; color: #8892B0;">Away</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)


                        
                    with col_m4:
                        st.caption(f"🕒 {m['formatted_date']}")
                        if st.button(labels["btn_simulate"], key=f"btn_sim_{idx}_{h_name[:3]}_{a_name[:3]}", type="primary"):
                            st.session_state["team_a_select"] = h_name
                            st.session_state["team_b_select"] = a_name
                            st.session_state["pending_nav"] = labels["nav_simulator"]
                            st.rerun()



                            
                    st.markdown("<hr style='margin: 0.8rem 0; border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)




    elif menu == labels["nav_raw"]:
        st.markdown(f"<div class='main-title'>{labels['raw_explorer']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtitle'>{labels['raw_explorer_desc']}</div>", unsafe_allow_html=True)
        
        # Filters row
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            search_team = st.text_input(labels["search_team"])
        with col_f2:
            select_league = st.multiselect(labels["filter_league"], ['A', 'B', 'C', 'D'], default=['A', 'B', 'C', 'D'])
            
        filtered_df = df.copy()
        if search_team:
            filtered_df = filtered_df[filtered_df['team'].str.contains(search_team, case=False)]
        if select_league:
            filtered_df = filtered_df[filtered_df['league'].isin(select_league)]
            
        st.dataframe(filtered_df, width="stretch")

    elif menu == labels["nav_docs"]:
        st.markdown(f"<div class='main-title'>{labels['nav_docs']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtitle'>{'Complete technical methodology and model descriptions' if lang == 'EN' else 'Kompletní metodika, výpočty a popis vizualizací a modelů'}</div>", unsafe_allow_html=True)
        
        doc_file = "DOCUMENTATION_EN.md" if lang == "EN" else "DOCUMENTATION.md"
        doc_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), doc_file)
        if os.path.exists(doc_path):
            with open(doc_path, 'r', encoding='utf-8') as f:
                doc_content = f.read()
            st.markdown(doc_content)
        else:
            st.error("Dokumentační soubor nenalezen!" if lang == "CZ" else "Documentation file not found!")


