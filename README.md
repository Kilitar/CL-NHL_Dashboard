# Premium Hockey Analytics & Betting Dashboard

This dashboard is a premium, standalone data application showcasing web scraping, data processing, statistical analysis, and interactive odds-making simulation.

## Project Structure
- `data/`: Contains raw HTML, interim JSON, and final processed CSV datasets.
- `src/`: Scraper, data processor, and odds analysis logic.
- `app.py`: Streamlit-based interactive dashboard with modern visualizations and simulator.

## Setup & Run
1. Make sure you have python installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the pipeline (scraping, processing, and analyzing):
   ```bash
   python run.py
   ```
4. Run the dashboard:
   ```bash
   streamlit run app.py
   ```
