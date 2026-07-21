import os
import sys

# Ensure project root is in python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.scraper import scrape_hockey_data
from src.processor import process_raw_data
from src.analysis import clean_and_analyze_data

def main():
    print("=== STARTING DATA PIPELINE ===")
    
    # 1. Fetch full NHL data from official API (1990 to current year)
    try:
        from src.fetch_full_nhl_data import fetch_full_nhl_data
        fetch_full_nhl_data()
    except Exception as e:
        print(f"API Fetch fallback to web scraping due to: {e}")
        raw_dir = os.path.join(project_root, "data", "raw")
        scrape_hockey_data(raw_dir)
        interim_file = os.path.join(project_root, "data", "interim", "hockey_teams.json")
        process_raw_data(raw_dir, interim_file)
        processed_file = os.path.join(project_root, "data", "processed", "hockey_teams.csv")
        clean_and_analyze_data(interim_file, processed_file)
    
    print("\n=== PIPELINE RUN COMPLETED SUCCESSFULY ===")

if __name__ == "__main__":
    main()
