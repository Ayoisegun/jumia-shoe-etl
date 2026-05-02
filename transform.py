import pandas as pd
import re
from datetime import datetime
pd.set_option("display.max_columns", None)

def transform(untransformed):
    raw = pd.DataFrame(untransformed)
    raw['Product_name'] = raw['Product_name'].str.strip()
    raw['Price'] = raw['Price'].str.replace(r'[^\d.]', '', regex=True).astype(float)
    ids = raw['Link'].str.extract(r'-(\d+)\.html')[0]
    raw['Id'] = (
        ids
        .fillna(raw['Link'].apply(lambda x: abs(hash(x))))
        .astype(str)
    )
    # raw['Id'] = raw['Link'].str.extract(r'-(\d+)\.html').astype('Int64') or hash(raw['Link'])
    raw['Discount'] = pd.to_numeric(raw['Discount'].str.rstrip('%'), errors='coerce').astype('Int64')
    today = datetime.now().strftime('%Y-%m-%d')
    raw['Date_Scraped'] = today
    raw["Date_Scraped"] = pd.to_datetime(raw["Date_Scraped"]).dt.date
    raw = raw[raw['Price'] < 1e8]
    return raw
    
