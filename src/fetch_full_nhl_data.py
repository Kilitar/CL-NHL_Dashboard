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
    
    records = []
    
    print(f"Found {len(seasons_data)} total seasons in NHL API.")
    
    for s in seasons_data:
        season_id = s.get("id")
        end_date = s.get("standingsEnd")
        
        # Filter for seasons from 1990 onwards (e.g. seasonId >= 19901991)
        start_year = int(str(season_id)[:4])
        if start_year < 1990 or start_year > 2025:
            continue
            
        print(f"Fetching standings for season {start_year} (End date: {end_date})...")
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
            
    df = pd.DataFrame(records)
    
    # Save to processed CSV
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, sep=';', index=False)
    print(f"Successfully updated {output_file} with {len(df)} total records from 1990 to {df['season'].max()}!")

if __name__ == "__main__":
    fetch_full_nhl_data()
