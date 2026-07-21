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
    
    # 1. Scrape data
    raw_dir = os.path.join(project_root, "data", "raw")
    scrape_hockey_data(raw_dir)
    
    # 2. Process HTML data to interim JSON
    interim_file = os.path.join(project_root, "data", "interim", "hockey_teams.json")
    process_raw_data(raw_dir, interim_file)
    
    # 3. Clean and analyze to processed CSV
    processed_file = os.path.join(project_root, "data", "processed", "hockey_teams.csv")
    clean_and_analyze_data(interim_file, processed_file)
    
    print("\n=== PIPELINE RUN COMPLETED SUCCESSFULY ===")

if __name__ == "__main__":
    main()
