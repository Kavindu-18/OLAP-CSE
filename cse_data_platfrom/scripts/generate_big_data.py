import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Settings
ROWS = 1_000_000  # 1 Million rows (Start small, increase if your laptop handles it)
START_DATE = datetime(2020, 1, 1)

def generate_data():
    print(f"Generating {ROWS} rows of dummy data...")
    
    # 1. Generate Dates
    date_range = [START_DATE + timedelta(days=x) for x in range((datetime.today() - START_DATE).days)]
    
    # 2. Create DataFrame with numpy (faster than loop)
    data = {
        'trade_id': np.arange(ROWS),
        'symbol': np.random.choice(['JKH', 'SAMP', 'COMB', 'HNB', 'DIAL'], ROWS),
        'price': np.round(np.random.uniform(50, 200, ROWS), 2),
        'volume': np.random.randint(10, 5000, ROWS),
        'trade_date': np.random.choice(date_range, ROWS)
    }
    
    df = pd.DataFrame(data)
    
    # 3. Save as CSV locally first
    output_path = "/opt/airflow/data/historical_trades.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved {ROWS} rows to {output_path}")

if __name__ == "__main__":
    generate_data()