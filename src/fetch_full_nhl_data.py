import os
import time
import requests
import pandas as pd

def fetch_full_nhl_data():
    """
    Fetches official NHL standings data from 1990 to 2025 using official NHL API.
    Saves and updates processed/hockey_teams.csv
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_file = os.path.join(base_dir, "data", "processed", "hockey_teams.csv")
    
    # Get available seasons from NHL API
    seasons_url = "https://api-web.nhle.com/v1/standings-season"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    response = requests.get(seasons_url, headers=headers)
    response.raise_for_status()
    seasons_data = response.json().get("seasons", [])
    
    # Incremental Load Check: Load existing dataset if available
    existing_df = None
    existing_seasons = set()
    if os.path.exists(output_file):
        try:
            existing_df = pd.read_csv(output_file, sep=';')
            if 'season' in existing_df.columns:
                existing_seasons = set(existing_df['season'].unique())
                print(f"[INCREMENTAL LOAD] Found existing dataset with {len(existing_seasons)} seasons ({min(existing_seasons)}-{max(existing_seasons)}).")
        except Exception as e:
            print(f"[INCREMENTAL LOAD] Could not read existing dataset for delta check: {e}")
            existing_df = None

    current_year = pd.Timestamp.now().year
    records = []
    
    print(f"Found {len(seasons_data)} total seasons in NHL API.")
    
    for s in seasons_data:
        season_id = s.get("id")
        end_date = s.get("standingsEnd")
        
        # Filter for seasons from 1990 onwards
        start_year = int(str(season_id)[:4])
        if start_year < 1990:
            continue
            
        # INCREMENTAL LOAD DELTA RULE:
        # Skip fetching if season is already fully ingested AND is not the current/latest ongoing season.
        if start_year in existing_seasons and start_year < (current_year - 1):
            continue
            
        print(f"[INCREMENTAL FETCH] Fetching delta for season {start_year} (End date: {end_date})...")
        standings_url = f"https://api-web.nhle.com/v1/standings/{end_date}"
        
        try:
            r = requests.get(standings_url, headers=headers, timeout=15)
            if r.status_code != 200:
                print(f"Warning: Failed to fetch {end_date} (Status {r.status_code})")
                continue
                
            teams_standings = r.json().get("standings", [])
            for t in teams_standings:
                t_name = t.get("teamName", {}).get("default") or t.get("placeName", {}).get("default", "Unknown")
                
                # If teamName default is only city (e.g., 'Colorado'), construct full name if teamCommonName present
                common_name = t.get("teamCommonName", {}).get("default", "")
                if common_name and common_name not in t_name:
                    full_name = f"{t_name} {common_name}"
                else:
                    full_name = t_name
                    
                wins = t.get("wins", 0)
                losses = t.get("losses", 0)
                ot_losses = t.get("otLosses", 0)
                ties = t.get("ties", 0)
                gf = t.get("goalFor", 0)
                ga = t.get("goalAgainst", 0)
                diff = t.get("goalDifferential", gf - ga)
                win_pct = round(t.get("winPctg", (wins / (wins + losses + ot_losses + ties)) if (wins + losses) > 0 else 0), 3)
                
                # Determine league category (A/B/C/D) based on win_pct quartiles for UI compatibility
                if win_pct >= 0.58:
                    league_cat = "A"
                elif win_pct >= 0.48:
                    league_cat = "B"
                elif win_pct >= 0.38:
                    league_cat = "C"
                else:
                    league_cat = "D"
                    
                records.append({
                    "team": full_name,
                    "season": start_year,
                    "victories": wins,
                    "defeats": losses,
                    "overtime_defeats": ot_losses,
                    "victory_percentage": win_pct,
                    "scored_goals": gf,
                    "received_goals": ga,
                    "goal_difference": diff,
                    "league": league_cat
                })
                
            time.sleep(0.3) # Polite API delay
        except Exception as err:
            print(f"Error fetching season {start_year}: {err}")
            
    new_df = pd.DataFrame(records) if len(records) > 0 else pd.DataFrame()
    
    if existing_df is not None and not existing_df.empty:
        if not new_df.empty:
            # Combine existing dataset with new fetched delta, keeping latest delta for overlaps
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df = combined_df.drop_duplicates(subset=['team', 'season'], keep='last')
        else:
            combined_df = existing_df
            print("[INCREMENTAL LOAD] No new delta needed. All historical seasons up to date.")
    else:
        combined_df = new_df
        
    df = combined_df.sort_values(['season', 'team']).reset_index(drop=True)
    
    # Clean up team names for consistency with UI logos/naming
    name_replacements = {
        "Mighty Ducks of Anaheim": "Mighty Ducks of Anaheim",
        "Anaheim Ducks": "Anaheim Ducks",
        "Phoenix Coyotes": "Phoenix Coyotes",
        "Arizona Coyotes": "Arizona Coyotes",
        "Utah Hockey Club": "Utah Hockey Club",
    }
    df["team"] = df["team"].replace(name_replacements)
    
    # Save log report
    log_file = os.path.join(base_dir, "pipeline_status.log")
    if df.empty:
        error_msg = "[CRITICAL ERROR] NHL dataset is empty! Pipeline execution failed."
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(error_msg + "\n")
        raise RuntimeError(error_msg)
        
    log_msg = f"[SUCCESS] Incremental Load complete. Updated {output_file} with {len(df)} records across {df['season'].nunique()} seasons (1990-{df['season'].max()})."
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(log_msg + "\n")
        
    # Save to processed CSV
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, sep=';', index=False)
    print(log_msg)

if __name__ == "__main__":
    fetch_full_nhl_data()
