"""
SIMPLE WEB SCRAPER FOR BEGINNERS
This is a simplified version to understand the basics
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

# Step 1: Setup browser
print("Starting browser...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Step 2: Open website
print("Opening website...")
driver.get("https://quotes.toscrape.com/")

# Step 3: Wait a bit for page to load
time.sleep(2)

# Step 4: Extract data
print("Extracting quotes...")
quotes_data = []

# Find all quote containers
quotes = driver.find_elements(By.CLASS_NAME, "quote")
print(f"Found {len(quotes)} quotes!")

# Loop through each quote
for quote in quotes:
    # Get the quote text
    quote_text = quote.find_element(By.CLASS_NAME, "text").text
    
    # Get the author name
    author = quote.find_element(By.CLASS_NAME, "author").text
    
    # Store in list
    quotes_data.append({
        "Quote": quote_text,
        "Author": author
    })
    
    print(f"✓ {author}")

# Step 5: Close browser
print("Closing browser...")
driver.quit()

# Step 6: Save to CSV
print("Saving to CSV...")
df = pd.DataFrame(quotes_data)
df.to_csv("quotes.csv", index=False)

print(f"\n✓ Done! Saved {len(quotes_data)} quotes to quotes.csv")
print("\nFirst 3 quotes:")
print(df.head(3))
