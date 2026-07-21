# 🏒 Analytics Documentation - Hockey Analytics Dashboard

This document provides a detailed methodological and technical description of all visualizations, metrics, mathematical formulas, and Machine Learning (ML) predictive models used in the **Hockey Analytics Dashboard** application.

---

## 🏗️ 1. Data Pipeline and Architecture (ETL)

The application processes historical hockey team data extracted from *Scrape This Site*. The data pipeline consists of three steps:

1. **Scraper (`src/scraper.py`)**: 
   - Downloads 24 HTML pages containing complete seasonal league results (582 team records in total).
2. **Processor (`src/processor.py`)**:
   - Parses HTML tables using `BeautifulSoup` and exports a structured JSON interim dataset.
3. **Analytics Module (`src/analysis.py`)**:
   - Cleans missing values (e.g. filling overtime loss defaults), casts data types, and **classifies teams into League Groups (A, B, C, D)** based on win percentage quantiles:
     - **Group A (Top 5%)**: Teams with overall win rate $\ge 95\%$ quantile.
     - **Group B (Strong Above Avg)**: Teams between $70\%$ and $95\%$ quantile.
     - **Group C (Mid Tier)**: Teams between $20\%$ and $70\%$ quantile.
     - **Group D (Bottom 20%)**: Teams with overall win rate $< 20\%$ quantile.

---

## ⚙️ 2. Sidebar Global Filters

- **Automatic Locale Detection & URL State Sync**:
  - Upon initial app launch, the application inspects the client browser's `Accept-Language` header to default to Czech or English.
  - Chosen language settings and selected team matchups in the simulator are synchronized into URL query parameters (`st.query_params`) and `st.session_state`, ensuring seamless state retention across page reloads (F5) and shareable deep links.
- **Actual Teams Only Checkbox**:
  - Restricts analysis strictly to active current NHL franchises.
  - Automatically filters out historical, relocated, or renamed team names (*Atlanta Thrashers, Hartford Whalers, Mighty Ducks of Anaheim, Minnesota North Stars, Phoenix Coyotes, Quebec Nordiques*).
- **Season Range Slider**:
  - Dynamically filters analyzed historical period (e.g. *1990 to 2011*).
  - Adjusting global filters instantly recalculates **all summary metrics, charts, correlation matrices, and ML model training** for the selected timeframe and team subset.



---

## 📊 3. Section: Dashboard Overview

### 📈 Core Summary Metrics (KPIs)

- **Total Teams**:
  - **Formula**: `df['team'].nunique()`
  - **Meaning**: Total number of unique hockey clubs present in the filtered historical period.
- **Total Seasons**:
  - **Formula**: `df['season'].nunique()`
  - **Meaning**: Total number of tracked league seasons in range.
- **Total Goals**:
  - **Formula**: `df['scored_goals'].sum()`
  - **Meaning**: Sum of all goals scored across all matches, teams, and seasons.
- **Avg Win %**:
  - **Formula**: `df['victory_percentage'].mean() * 100`
  - **Meaning**: Average win percentage across all seasonal team records.

---

### 📉 Chart 1: Goals vs Victories Correlation (Scatter Plot)
- **Visualization Type**: Scatter Plot
- **X Axis**: Goals Scored (`Goals For - GF`)
- **Y Axis**: Season Victories (`Victories`)
- **Color Coding**: League Group (A, B, C, D)
- **Methodology & Meaning**:
  - Displays the relationship between offensive scoring efficiency and overall seasonal victories.

---

### 📦 Chart 2: Victories by League Category (Box Plot)
- **Visualization Type**: Box Plot with individual observation scatter (`points='all'`)
- **X Axis**: League Group (A, B, C, D)
- **Y Axis**: Victories (`Victories`)
- **Methodology & Meaning**:
  - Displays statistical distribution of victories within each league performance tier (median, IQR, outliers).

---

### 🌡️ Chart 3: Metrics Correlation Heatmap
- **Visualization Type**: Interactive Heatmap (`px.imshow`)
- **Mathematical Formula (Pearson Correlation Coefficient)**:
  $$r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}$$
- **Variables**: Scored Goals, Conceded Goals, Wins, Losses, Goal Difference (+/-), Win %.
- **Filtering Modes**:
  - **Entire League (All Teams)**: Computes macro-correlations across all teams in the league.
  - **Specific Team (e.g. Boston Bruins)**: Recalculates the correlation matrix exclusively for that selected team's historical records.
- **Meaning**: Quantifies linear dependencies between numerical metrics on both global league-wide and individual team levels.


---

### 📈 Chart 4: Multi-Team Trend Comparison (Line Chart)
- **Visualization Type**: Multi-trace Time-series Line Chart
- **X Axis**: Season (`Season`)
- **Y Axis**: Victories / Losses count
- **Methodology & Meaning**:
  - Allows selecting **Team 1** and optionally **Team 2** to visually compare historical win and loss trajectories side-by-side.

---

## 🎲 4. Section: Odds Calculator & Predictive ML Models

Simulates a matchup between two selected teams (Home vs. Away) and offers 3 analytical sub-tabs.

### ⚽ Tab 1: Moneyline (Win / Loss)
1. **Factoring Home Ice Advantage & Goalie Impact**:
   $$P_{\text{adj}}(A) = P(A) \cdot \left(1 + \frac{\text{HomeAdvantage}\%}{100}\right) \cdot \left(1 + \frac{\text{GoalieImpact}\%}{100}\right)$$
   Probabilities are then normalized so that $P_{\text{adj}}(A) + P_{\text{adj}}(B) = 1$.
2. **Raw Odd**:
   $$\text{Odd}_{\text{raw}} = \frac{1}{P_{\text{adj}}(\text{Win})}$$
3. **Adjusted Odd with Margin**:
   $$\text{Odd}_{\text{adj}} = \max\left(1.01, \text{Odd}_{\text{raw}} \cdot (1 - \text{Margin})\right)$$

---

### 🧮 Tab 2: Over / Under (Poisson Goal Model)
Models total match goals using the **Poisson Distribution**:
- **Expected Goals per Match ($\lambda$)**:
  $$\lambda_{\text{home}} = \frac{\text{GoalsFor}_{\text{home}} + \text{GoalsAgainst}_{\text{away}}}{2 \cdot 82} \cdot 1.05$$
  $$\lambda_{\text{away}} = \frac{\text{GoalsFor}_{\text{away}} + \text{GoalsAgainst}_{\text{home}}}{2 \cdot 82}$$
  $$\lambda_{\text{total}} = \lambda_{\text{home}} + \lambda_{\text{away}}$$
- **Cumulative Probability for Under X Goals**:
  $$P(\text{Under } X) = \sum_{k=0}^{\lfloor X \rfloor} \frac{\lambda_{\text{total}}^k e^{-\lambda_{\text{total}}}}{k!}$$
  $$P(\text{Over } X) = 1 - P(\text{Under } X)$$

---

### 💰 Tab 3: EV & Kelly Calculator (Value Betting & Bankroll Management)
Compares model fair odds with bookmaker market odds to estimate expected value and exact stake tailored to the user's Bankroll:
1. **Expected Value (EV %)**:
   $$\text{EV \%} = (P_{\text{model}} \cdot \text{Odd}_{\text{market}} - 1) \cdot 100\%$$
   *If $\text{EV} > 0\%$, the bet represents a positive Value Bet.*
2. **Kelly Criterion & Bet Sizing (Half-Kelly)**:
   The Kelly formula calculates the mathematically optimal fraction $f^*$ of the bankroll to wager to maximize long-term bankroll growth while preventing bankruptcy. The app applies the conservative **Half-Kelly (50% of full Kelly)**:
   $$f^* = \max\left(0, \frac{P_{\text{model}} \cdot \text{Odd}_{\text{market}} - 1}{\text{Odd}_{\text{market}} - 1}\right) \cdot 0.5$$
   $$\text{Recommended Stake (\$)} = \text{Bankroll} \cdot f^*$$
3. **Practical Interpretation**:
   - The user configures their **Virtual Bankroll** in the sidebar (e.g. *$10,000*).
   - For market odds of **2.10** and model win chance of **60%**, the calculator evaluates $\text{EV} = +26.00\%$ and recommends wagering **$1,182** ($11.8\%$ of bankroll).
   - If market odds offer no value ($\text{EV} \le 0\%$), recommended stake is **$0**.

---


### 🤖 Predictive Models in Simulator

1. **Historical Baseline**: Overall historical win rate comparison.
2. **Rolling Form (Last 3 Seasons)**: 3-season rolling averages of win percentage and goals.
3. **Logistic Regression (ML Model)**: Statistical classifier from `scikit-learn` trained on win percentage and goal differential gaps.
4. **Random Forest Classifier (Advanced ML)**: Ensemble decision tree classifier (100 trees) capturing non-linear interactions.

---

### 📊 Chart 5: Predictive ML Models Comparison (Grouped Bar Chart)
- Compares win probability estimates across all 4 models.
- Features multi-line tooltips displaying untruncated team names.

---

## 📅 5. Section: Upcoming NHL Match Schedule

- **Live REST API Integration (`src/schedule.py`)**:
  - Fetches real-time scheduled games directly from official NHL REST API (`https://api-web.nhle.com/v1/schedule/now`).
- **Team Branding & Color Contrast (`src/logos.py`)**:
  - Leverages `src/logos.py` to dynamically fetch official NHL logos and primary franchise color codes.
  - Features a high-contrast **Fire vs. Ice** color scheme: Home Team is styled in Coral Red (`#FF4B4B`), Away Team in Ice Blue (`#38BDF8`).
- **1-Click Match Simulation**:
  - Each matchup card renders official team logos, home/away designation, and kickoff date/time (UTC).
  - Clicking **`⚡ Simulate Match in Calculator`** instantly pre-loads the matchup into the Odds Calculator and redirects the user automatically.

---


## 🗃️ 6. Section: Raw Data Explorer

- **Search Input (`Search Team Name`)**: Real-time team filtering.
- **League Filter (`Filter by League Group`)**: Interactive selection of groups A, B, C, D.
- **Interactive Table (`st.dataframe`)**: Complete cleaned dataset containing all 582 records filtered by season range.

---

## ⚙️ 7. MLOps & Automated Data Pipeline (GitHub Actions)

The `.github/workflows/scrape_data.yml` file provides full pipeline automation:
- **Weekly cron schedule (`0 0 * * 0`)** and manual trigger support from GitHub UI.
- Executes `python run.py`, fetches raw HTML pages, and updates interim JSON and final CSV files.
- Automatically commits and pushes updated datasets back to the repository whenever new data is detected.
