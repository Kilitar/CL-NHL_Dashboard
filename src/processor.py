import os
import json
import glob
from bs4 import BeautifulSoup

def process_raw_data(raw_dir="data/raw", output_file="data/interim/hockey_teams.json"):
    """
    Parses downloaded HTML files and converts them to a structured JSON format.
    """
    raw_path_pattern = os.path.join(raw_dir, "*.html")
    files = sorted(glob.glob(raw_path_pattern))
    
    if not files:
        print(f"No HTML files found in {raw_dir}!")
        return
        
    data = []
    print(f"Processing {len(files)} HTML files...")
    
    for file in files:
        print(f"Parsing {os.path.basename(file)}...")
        with open(file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        table = soup.find('table')
        if not table:
            continue
            
        headers = [cell.text.strip() for cell in table.find_all('th')]
        
        for row in table.find_all('tr', class_='team'):
            cells = row.find_all('td')
            cells_text = [cell.text.strip() for cell in cells]
            
            # Match headers and cells
            record = dict(zip(headers, cells_text))
            data.append(record)
            
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
    print(f"Processed data saved to {output_file}. Total records: {len(data)}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    process_raw_data(
        raw_dir=os.path.join(base_dir, "data", "raw"),
        output_file=os.path.join(base_dir, "data", "interim", "hockey_teams.json")
    )
