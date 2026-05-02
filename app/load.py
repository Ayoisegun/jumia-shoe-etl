import psycopg2
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy.exc import OperationalError
import time

load_dotenv()


conn_params = {
    "host": os.getenv("DB_HOST", "localhost"),        
    "database": "products_pipeline",      
    "user": os.getenv("DB_USER"),    
    "password": os.getenv("DB_PASSWORD")
}

def load(transformed_df):
    conn_string = f"postgresql://{conn_params['user']}:{conn_params['password']}@{conn_params['host']}/{conn_params['database']}"
    engine = create_engine(conn_string)
    retries = 5
    while retries > 0:
        try:
            # Try to connect
            with engine.connect() as conn:
                print("Connection successful!")
                break 
        except OperationalError:
            retries -= 1
            print(f"Waiting for database... ({retries} retries left)")
            time.sleep(5) # Wait 5 seconds before trying again
    if retries == 0:
        raise Exception("Could not connect to the database after several attempts.")

    # 1. Load the entire dataframe to a staging table
    transformed_df.to_sql('temp_staging', engine, if_exists='replace', index=False)

    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS price_logs (
                product_id TEXT REFERENCES products(id) ON DELETE CASCADE,
                price NUMERIC NOT NULL,
                discount INTEGER,
                timestamp DATE NOT NULL,
                UNIQUE(product_id, timestamp)
            );
        """))
        conn.commit()

    with engine.connect() as conn:
        # 2. Insert NEW products only (skip if ID exists)
        conn.execute(text("""
            INSERT INTO products (id, name)
            SELECT DISTINCT "Id", "Product_name" FROM temp_staging
            ON CONFLICT (id) DO NOTHING;
        """))

        # 3. Insert the daily price log
        conn.execute(text("""
            INSERT INTO price_logs (product_id, price, discount, timestamp)
            SELECT "Id", "Price", "Discount", "Date_Scraped" FROM temp_staging
            ON CONFLICT (product_id, timestamp) DO NOTHING;
        """))
        
        # Explicitly commit changes if not using autocommit
        conn.commit()
    
    print("Database Load Complete!")