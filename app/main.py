import pandas as pd
from extract import extract_jumia_data
from transform import transform
from dotenv import load_dotenv
load_dotenv()
from load import load


pd.set_option("display.max_columns", None)

# =========================
# 1. CONFIGURATION
# =========================
MAX_PAGES = 5

base_url = "https://www.jumia.com.ng/fragment/sp/products/provider/mirakl/catalog-page-types/category/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.jumia.com.ng/mens-shoes/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

params = {
    "fq": '{"category":10169}',
    "page": 1,
    "numberItems": 40,
    "viewType": "grid",
    "lang": "en",
    "returnOverride": "https://www.jumia.com.ng/mens-shoes/"
}

def run_pipeline():
    # 1. Extract
    untransformed = extract_jumia_data(base_url, params, headers, MAX_PAGES)
    
    # 2. Transform
    if untransformed:
        transformed_jumia = transform(untransformed)
        print(transformed_jumia.head())
        
        # 3. Load
        print(f"Total items scraped across all pages: {len(transformed_jumia)}")
        print(f"Unique product IDs: {transformed_jumia['Id'].nunique()}")
        load(transformed_jumia)

if __name__ == "__main__":
    run_pipeline()
