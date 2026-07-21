# 🏒 Dokumentace analytického dashboardu Hockey Analytics

Tento dokument poskytuje podrobný metodický a technický popis všech vizualizací, metrik, matematických vzorců a prediktivních modelů strojového učení (ML) použitých v aplikaci **Hockey Analytics Dashboard**.

---

## 🏗️ 1. Datová pipeline a architektura (ETL)

Aplikace zpracovává historická data hokejových týmů získaná ze serveru *Scrape This Site*. Datová pipeline se skládá ze tří kroků:

1. **Scraper (`src/scraper.py`)**: 
   - Stahuje 24 stránek HTML s kompletními výsledky ligových sezón (celkem 582 záznamů týmů).
2. **Procesor (`src/processor.py`)**:
   - Pomocí `BeautifulSoup` parsuje HTML tabulky a ukládá strukturovaný JSON mezisoubor.
3. **Analytický modul (`src/analysis.py`)**:
   - Čistí chybějící hodnoty (např. doplnění nul u proher v prodloužení), převádí datové typy a **kategorizuje týmy do ligových skupin (A, B, C, D)** podle kvantilů úspěšnosti výher:
     - **Skupina A (Top 5 %)**: Týmy s celkovou úspěšností $\ge 95\%$ kvantilu.
     - **Skupina B (Silný nadprůměr)**: Týmy mezi $70\%$ a $95\%$ kvantilm.
     - **Skupina C (Průměr / Střed)**: Týmy mezi $20\%$ a $70\%$ kvantilm.
     - **Skupina D (Spodních 20 %)**: Týmy s celkovou úspěšností $< 20\%$ kvantilu.

---

## ⚙️ 2. Globální filtry bočního panelu

- **Automatická detekce jazyka & Persistování (Locale & URL Sync)**:
  - Při prvním načtení aplikace skript automaticky detekuje preferovaný jazyk z hlavičky prohlížeče klienta (`Accept-Language`).
  - Vybrané nastavení jazyka i zvolená dvojice týmů v simulátoru se automaticky ukládá do URL parametrů (`st.query_params`) a relace uživatele (`st.session_state`), což garantuje zachování stavu i při obnovení stránky (F5) nebo přímém sdílení odkazů.
- **Pouze současné týmy (Actual teams only)**:
  - Zahrne do analýzy výhradně aktivní současné týmy NHL.
  - Automaticky odfiltruje zaniklé, přesídlené nebo historicky přejmenované franšízy (*Atlanta Thrashers, Hartford Whalers, Mighty Ducks of Anaheim, Minnesota North Stars, Phoenix Coyotes, Quebec Nordiques*).
- **Rozsah sezón (Season Range)**:
  - Umožňuje dynamicky omezit analyzované období (např. *1990 až 2011*).
  - Při změně filtrů se okamžitě přepočítají **všechny metriky, grafy, korelační matice i trénování ML modelů** pro vybranou časovou epochu a podmnožinu týmů.



---

## 📊 3. Sekce: Dashboard (Přehledový panel)

### 📈 Klíčové souhrnné metriky (KPIs)

- **Celkem týmů (Total Teams)**:
  - **Vzorec**: `df['team'].nunique()`
  - **Význam**: Udává celkový počet unikátních hokejových klubů ve vybraném období.
- **Celkem sezón (Total Seasons)**:
  - **Vzorec**: `df['season'].nunique()`
  - **Význam**: Počet sledovaných ligových ročníků.
- **Góly celkem (Total Goals)**:
  - **Vzorec**: `df['scored_goals'].sum()`
  - **Význam**: Celkový součet všech vstřelených gólů napříč všemi zápasy a týmy.
- **Průměrná výhra % (Avg Win %)**:
  - **Vzorec**: `df['victory_percentage'].mean() * 100`
  - **Význam**: Průměrná procentuální úspěšnost výher ze všech sezónních záznamů.

---

### 📉 Graf 1: Korelace gólů a výher (Scatter Plot)
- **Typ vizualizace**: Bodový graf (Scatter Plot)
- **Osa X**: Počet vstřelených gólů (`Goals For - GF`)
- **Osa Y**: Počet vítězství v sezóně (`Victories`)
- **Barevné rozlišení**: Ligová skupina (A, B, C, D)
- **Metodika a význam**:
  - Graf zobrazuje vztah mezi útočnou produktivitou týmu a jeho celkovým počtem výher v sezóně.
  - Umožňuje identifikovat efektivitu týmů (útočně vs. obranně zaměřené kluby).

---

### 📦 Graf 2: Počet výher podle ligové kategorie (Box Plot)
- **Typ vizualizace**: Krabicový graf (Box Plot s rozptylem jednotlivých pozorování `points='all'`)
- **Osa X**: Ligová skupina (A, B, C, D)
- **Osa Y**: Počet vítězství (`Victories`)
- **Metodika a význam**:
  - Zobrazuje statistické rozdělení výher uvnitř jednotlivých ligových výkonnostních tříd (medián, IQR, odlehlé hodnoty).

---

### 🌡️ Graf 3: Korelační matice metrik (Heatmapa)
- **Typ vizualizace**: Interaktivní Heatmapa (`px.imshow`)
- **Matematický princip (Pearsonův korelační koeficient)**:
  $$r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}$$
- **Sledované proměnné**: Vstřelené góly, obdržené góly, výhry, prohry, brankový rozdíl (+/-), % výher.
- **Režimy filtrování**:
  - **Celá liga (Všechny týmy)**: Počítá makro-korelaci napříč všemi kluby ligy.
  - **Specifický tým (např. Boston Bruins)**: Přepočítá korelační matici výhradně pro historická data zvoleného klubu.
- **Význam**: Přesně kvantifikuje lineární závislosti mezi metrikami v celoligovém i týmovém měřítku.


---

### 📈 Graf 4: Srovnávací historická analýza týmů (Multi-Team Line Chart)
- **Typ vizualizace**: Čárový časový graf (Line Chart) s podporou srovnání 2 týmů.
- **Osa X**: Sezóna (`Season`)
- **Osa Y**: Počet vítězství / proher
- **Metodika a význam**:
  - Umožňuje zvolit **Tým 1** a volitelně **Tým 2** pro přímou vizuální konfrontaci historických výherních a proherních linií obou klubů v čase.

---

## 🎲 4. Sekce: Sázková kalkulačka & Prediktivní ML modely

Sekce simuluje zápas dvou vybraných týmů (Domácí vs. Hosté) a nabízí 3 analytické pod-záložky.

### ⚽ Záložka 1: Moneyline (Výhra / Prohra)
1. **Započtení výhody domácího ledu & vlivu brankáře**:
   $$P_{\text{adj}}(A) = P(A) \cdot \left(1 + \frac{\text{HomeAdvantage}\%}{100}\right) \cdot \left(1 + \frac{\text{GoalieImpact}\%}{100}\right)$$
   Pravděpodobnosti jsou následně normalizovány tak, aby jejich součet tvořil přesně 1.
2. **Čistý kurz (Raw Odd)**:
   $$\text{Odd}_{\text{raw}} = \frac{1}{P_{\text{adj}}(\text{Výhra})}$$
3. **Kurz s marží bookmakera (Adjusted Odd)**:
   $$\text{Odd}_{\text{adj}} = \max\left(1.01, \text{Odd}_{\text{raw}} \cdot (1 - \text{Marže})\right)$$

---

### 🧮 Záložka 2: Over / Under (Poissonův model gólů)
Modeluje pravděpodobnosti počtu gólů v zápase pomocí **Poissonova rozdělení**:
- **Očekávané góly na zápas ($\lambda$)**:
  $$\lambda_{\text{domácí}} = \frac{\text{StřelenéGóly}_{\text{domácí}} + \text{ObdrženéGóly}_{\text{hosté}}}{2 \cdot 82} \cdot 1.05$$
  $$\lambda_{\text{hosté}} = \frac{\text{StřelenéGóly}_{\text{hosté}} + \text{ObdrženéGóly}_{\text{domácí}}}{2 \cdot 82}$$
  $$\lambda_{\text{celkem}} = \lambda_{\text{domácí}} + \lambda_{\text{hosté}}$$
- **Kumulativní pravděpodobnost Under X gólů**:
  $$P(\text{Under } X) = \sum_{k=0}^{\lfloor X \rfloor} \frac{\lambda_{\text{celkem}}^k e^{-\lambda_{\text{celkem}}}}{k!}$$
  $$P(\text{Over } X) = 1 - P(\text{Under } X)$$

---

### 💰 Záložka 3: EV & Kellyho kalkulačka (Value Betting & Bankroll Management)
Umožňuje porovnat modelový fér kurz s tržním kurzem sázkové kanceláře a spočítat přesnou výši sázky přizpůsobenou zadanému rozpočtu (Bankrollu):
1. **Očekávaná hodnota (Expected Value - EV %)**:
   $$\text{EV \%} = (P_{\text{model}} \cdot \text{Kurz}_{\text{trh}} - 1) \cdot 100\%$$
   *Pokud je $\text{EV} > 0\%$, jedná se o matematicky ziskovou Value bet sázku.*
2. **Kellyho kritérium & Výpočet sázky (Half-Kelly)**:
   Kellyho vzorec určuje matematicky optimální procento rozpočtu $f^*$ k vsazení pro maximální dlouhodobý růst bankrollu při minimálním riziku bankrotu. Aplikace využívá konzervativní **Half-Kelly (50 % z plného Kelly)**:
   $$f^* = \max\left(0, \frac{P_{\text{model}} \cdot \text{Kurz}_{\text{trh}} - 1}{\text{Kurz}_{\text{trh}} - 1}\right) \cdot 0.5$$
   $$\text{Doporučená sázka (Kč)} = \text{Bankroll} \cdot f^*$$
3. **Praktická interpretace**:
   - Uživatel v bočním panelu nastaví **Fiktivní rozpočet / Bankroll** (např. *10 000 Kč*).
   - Při kurzu bookmakera **2.10** a šanci výhry **60 %** spočítá kalkulačka $\text{EV} = +26.00\%$ a doporučí vsadit **1 182 Kč** ($11.8\%$ z bankrollu).
   - Pokud je kurz nevýhodný ($\text{EV} \le 0\%$), doporučená sázka je **0 Kč**.

---


### 🤖 Prediktivní modely v simulátoru

1. **Historické statistiky (Baseline)**: Celkový historický poměr výher obou týmů.
2. **Klouzavé průměry (Forma z 3 sezón)**: Klouzavé průměry výher a gólů z posledních 3 sezón.
3. **Logistická regrese (ML Model)**: Statistický model ze `scikit-learn` trénovaný na rozdílech v úspěšnosti a brankovém rozdílu.
4. **Random Forest Classifier (Pokročilé ML)**: Souborový rozhodovací model (100 stromů) zachycující nelineární závislosti.

---

### 📊 Graf 5: Porovnání predikcí všech ML modelů (Grouped Bar Chart)
- Srovnává odhady pravděpodobností výher obou týmů pro všechny 4 modely.
- Obsahuje víceliniový tooltip s celým názvem týmu bez ořezání.

---

## 📅 5. Sekce: Kalendář nadcházejících zápasů NHL

- **Živá integrace REST API (`src/schedule.py`)**:
  - V reálném čase stahuje plánované zápasy přímo z oficiálního API NHL (`https://api-web.nhle.com/v1/schedule/now`).
- **Barevné rozlišení a týmový branding (`src/logos.py`)**:
  - Využívá modul `src/logos.py` pro dynamické stahování oficiálních log klubů NHL a jejich primárních klubových barev.
  - Zavedeno kontrastní schémátko **Fire vs. Ice**: Domácí tým je vyobrazen v korálově červené (`#FF4B4B`), hosté v ledově modré (`#38BDF8`).
- **1-klik simulace**:
  - Každá karta zápasu zobrazuje logo a název domácího i hostujícího týmu, datum a přesný čas utkání (UTC).
  - Tlačítko **`⚡ Simulovat zápas v kalkulačce`** okamžitě přednastaví zvolené týmy do sázkové kalkulačky a přesměruje uživatele do simulátoru.

---


## 🗃️ 6. Sekce: Průzkumník hrubých dat (Raw Data Explorer)

- **Vyhledávací pole (`Search Team Name`)**: Umožňuje filtrovat tabulku podle názvu hokejového klubu v reálném čase.
- **Ligový filtr (`Filter by League Group`)**: Interaktivní výběr skupin A, B, C, D.
- **Interaktivní tabulka (`st.dataframe`)**: Zobrazuje kompletní vyčištěný datový soubor se všemi záznamy přizpůsobený nastavenému rozsahu sezón.

---

## ⚙️ 7. MLOps & Automatizace datové pipeline (GitHub Actions)

Soubor `.github/workflows/scrape_data.yml` zajišťuje plnou automatizaci datového toku:
- **Týdenní cron plán (`0 0 * * 0`)** a možnost ručního spuštění z GitHub UI.
- Spustí `python run.py`, stagne nejnovější HTML stránky a zaktualizuje CSV.
- V případě detekce nových dat skript automaticky vytvoří commit a push do repozitáře.

