import os
import time
import requests
from bs4 import BeautifulSoup

def scrape_hockey_data(output_dir="data/raw"):
    """
    Scrapes hockey team data from Scrape This Site (Forms and Pages pagination).
    Saves raw HTML files to output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)
    url_template = "https://www.scrapethissite.com/pages/forms/?page_num={page}"
    page = 1
    
    print("Starting scraping process...")
    while True:
        url = url_template.format(page=page)
        print(f"Fetching page {page}: {url}")
        
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        
        # Check if the table is empty (e.g. only header exists or table not found)
        if not table:
            print("No table found. Ending scrape.")
            break
            
        rows = table.find_all('tr')
        # Header is usually row 0, teams are in row 1+
        # If there are only header rows, the table is empty.
        team_rows = table.find_all('tr', class_='team')
        if len(team_rows) == 0:
            print(f"Page {page} has no team data. Ending scrape.")
            break
            
        page_str = str(page).zfill(2)
        filename = os.path.join(output_dir, f"hockey_teams_page_{page_str}.html")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print(f"Saved {filename}")
        page += 1
        time.sleep(1) # Polite delay

    print(f"Scraping complete. Total pages scraped: {page - 1}")

if __name__ == "__main__":
    # If run directly, scrape to project-local directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scrape_hockey_data(os.path.join(base_dir, "data", "raw"))
