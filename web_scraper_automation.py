"""
Web Scraping Automation Tool using Selenium
Scrapes product data from e-commerce website and exports to CSV
"""

import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

WEBSITE_URL = "https://quotes.toscrape.com/"

class WebScraperAutomation:
    """Automates web scraping using Selenium WebDriver"""
    
    def __init__(self):
        self.driver = None
        self.data = []
        
    def setup_driver(self):
        """Setup Chrome WebDriver with options"""
        print("[INFO] Setting up Chrome WebDriver...")
        chrome_options = webdriver.ChromeOptions()
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        print("[SUCCESS] WebDriver initialized")
        
    def scrape_quotes(self, num_pages=3):
        """Scrape quotes from website"""
        print(f"[INFO] Starting to scrape {num_pages} pages...")
        
        for page_num in range(1, num_pages + 1):
            try:
                if page_num == 1:
                    url = WEBSITE_URL
                else:
                    url = f"{WEBSITE_URL}page/{page_num}/"
                
                print(f"\n[PAGE {page_num}] Navigating to: {url}")
                self.driver.get(url)
                
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))
                )
                
                quotes = self.driver.find_elements(By.CLASS_NAME, "quote")
                print(f"[PAGE {page_num}] Found {len(quotes)} quotes")
                
                for idx, quote in enumerate(quotes, 1):
                    try:
                        quote_text = quote.find_element(By.CLASS_NAME, "text").text.strip('"')
                        author = quote.find_element(By.CLASS_NAME, "author").text.replace("--", "").strip()
                        tags_elements = quote.find_elements(By.CLASS_NAME, "tag-item")
                        tags = ", ".join([tag.text for tag in tags_elements])
                        
                        self.data.append({
                            "Quote": quote_text,
                            "Author": author,
                            "Tags": tags,
                            "Page": page_num
                        })
                        
                        print(f"  [{idx}] ✓ Scraped: {author}")
                        
                    except Exception as e:
                        print(f"  [ERROR] Failed to extract quote {idx}: {e}")
                
                time.sleep(2)
                
            except Exception as e:
                print(f"[ERROR] Failed to process page {page_num}: {e}")
                continue
        
        print(f"\n[SUCCESS] Total quotes scraped: {len(self.data)}")
        
    def clean_data(self):
        """Data cleaning and validation"""
        print("[INFO] Cleaning data...")
        
        if not self.data:
            print("[WARNING] No data to clean")
            return
        
        initial_count = len(self.data)
        self.data = [dict(t) for t in {tuple(d.items()) for d in self.data}]
        removed = initial_count - len(self.data)
        
        if removed > 0:
            print(f"[INFO] Removed {removed} duplicate entries")
        
        print(f"[SUCCESS] Data cleaned. Final records: {len(self.data)}")
        
    def save_to_csv(self, filename="quotes_data.csv"):
        """Save scraped data to CSV file"""
        if not self.data:
            print("[ERROR] No data to save")
            return
        
        try:
            df = pd.DataFrame(self.data)
            df.to_csv(filename, index=False)
            print(f"[SUCCESS] Data saved to {filename}")
            print(f"\nData Preview:")
            print(df.head())
            
        except Exception as e:
            print(f"[ERROR] Failed to save CSV: {e}")
    
    def close_driver(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()
            print("[INFO] WebDriver closed")
    
    def run(self, num_pages=3, output_file="quotes_data.csv"):
        """Execute the complete automation workflow"""
        try:
            self.setup_driver()
            self.scrape_quotes(num_pages)
            self.clean_data()
            self.save_to_csv(output_file)
            
        except Exception as e:
            print(f"[CRITICAL ERROR] {e}")
        finally:
            self.close_driver()

if __name__ == "__main__":
    print("=" * 70)
    print("WEB SCRAPING AUTOMATION TOOL")
    print("=" * 70)
    
    scraper = WebScraperAutomation()
    scraper.run(num_pages=3, output_file="quotes_data.csv")
    
    print("\n" + "=" * 70)
    print("AUTOMATION COMPLETE")
    print("=" * 70)
