import pandas as pd
import random
from datetime import datetime
import os

# Mock Data for Colombo Stock Exchange
COMPANIES = ['JKH', 'SAMP', 'COMB', 'HNB', 'DIAL']

def extract_data(execution_date):
    """
    Generates dummy trade data for a given date and saves it to CSV.
    """
    print(f"Extracting data for {execution_date}...")
    
    data = []
    for _ in range(100):  # Simulate 100 trades
        trade = {
            'symbol': random.choice(COMPANIES),
            'price': round(random.uniform(50, 200), 2),
            'volume': random.randint(100, 5000),
            'trade_time': f"{execution_date} {random.randint(9,14)}:{random.randint(0,59)}:00"
        }
        data.append(trade)
    
    df = pd.DataFrame(data)
    
    # Save to "Staging Area" (Local folder for now, S3 later)
    filename = f"/opt/airflow/data/trades_{execution_date}.csv"
    df.to_csv(filename, index=False)
    print(f"Saved to {filename}")

if __name__ == "__main__":
    # Allow passing date as argument
    import sys
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.today().strftime('%Y-%m-%d')
    extract_data(date)