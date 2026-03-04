import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime
from typing import List, Dict

# --- CONFIGURATION ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PriceMonitor:
    """
    Senior-level Price Intelligence Engine.
    Handles data extraction, normalization, and reporting.
    """
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,pl;q=0.8"
        }
        self.results: List[Dict] = []

    def fetch_data(self, url: str) -> BeautifulSoup:
        """Fetches page content with custom headers to avoid detection."""
        try:
            logging.info(f"Fetching data from: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            logging.error(f"Failed to fetch {url}: {str(e)}")
            return None

    def normalize_price(self, raw_price: str) -> float:
        """Cleans price string and converts to float."""
        try:
            # Removes currency symbols, spaces and replaces comma with dot
            clean_price = ''.join(c for c in raw_price if c.isdigit() or c in '.,')
            clean_price = clean_price.replace(',', '.')
            return float(clean_price)
        except ValueError:
            return 0.0

    def parse_example_site(self, soup: BeautifulSoup):
        """
        Generic parsing logic. 
        In a real scenario, this would target specific CSS selectors.
        """
        if not soup: return
        
        # Simulated data extraction for portfolio purposes
        # Let's assume we found some product elements
        mock_products = [
            {"name": "Professional Laptop Pro", "price": "4.500,00 PLN"},
            {"name": "Wireless Mouse Master", "price": "299,00 PLN"},
            {"name": "4K Monitor Business", "price": "1.850,50 PLN"}
        ]
        
        for item in mock_products:
            self.results.append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Product Name": item["name"],
                "Competitor Price": self.normalize_price(item["price"]),
                "Currency": "PLN",
                "Status": "Active"
            })
        
        logging.info(f"Successfully parsed {len(mock_products)} products.")

    def export_to_excel(self, filename: str = "Price_Report.xlsx"):
        """Saves collected data into a formatted Excel file."""
        if not self.results:
            logging.warning("No data to export.")
            return

        df = pd.DataFrame(self.results)
        df.to_excel(filename, index=False)
        logging.info(f"Report saved successfully: {filename}")

if __name__ == "__main__":
    # Initialize the Engine
    bot = PriceMonitor()
    
    # Process target (Example)
    # bot.fetch_data("https://competitor-webshop.com/deals")
    bot.parse_example_site(None) # Using mock data for demonstration
    
    # Finalize
    bot.export_to_excel()
    print("\n--- JOB COMPLETED SUCCESSFULLY ---")
