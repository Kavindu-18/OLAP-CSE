import pandas as pd
from sqlalchemy import create_engine
import sys

# Connection to our Docker Postgres
DB_CONN = "postgresql://user:password@postgres:5432/cse_dwh"

def load_data(execution_date):
    print(f"Loading data for {execution_date}...")
    
    # 1. Read the CSV from Staging
    filename = f"/opt/airflow/data/trades_{execution_date}.csv"
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print("No file found. Skipping.")
        return

    engine = create_engine(DB_CONN)

    # 2. IDEMPOTENCY: Delete existing data for this date!
    # In a real job, you'd use a date column. Here we assume we process daily.
    # (Simplified for tutorial: We are just appending for now, but in prod, we run a DELETE SQL first)
    
    # 3. Write to Database
    # We use 'append' because we handle deduplication via the DELETE step (skipped for brevity)
    df.to_sql('staging_trades', engine, if_exists='append', index=False)
    print("Data loaded successfully.")

if __name__ == "__main__":
    date = sys.argv[1]
    load_data(date)