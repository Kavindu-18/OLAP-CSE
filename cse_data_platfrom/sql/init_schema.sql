-- 1. Create the Dimension: Companies
CREATE TABLE dim_company (
    company_sk SERIAL PRIMARY KEY,       -- Surrogate Key (Our internal ID)
    symbol VARCHAR(10) NOT NULL,         -- Business Key (e.g., 'JKH')
    company_name VARCHAR(255),
    sector VARCHAR(100),
    is_current BOOLEAN DEFAULT TRUE,     -- For handling history (SCD Type 2)
    start_date DATE DEFAULT CURRENT_DATE,
    end_date DATE
);

-- 2. Create the Dimension: Date
-- Why? Asking "Get me Q1 2024 sales" is slow if you have to calculate
-- dates every time. We pre-calculate quarters, weekends, and holidays here.
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,            -- Format: 20240207
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    day_of_week INT,
    is_trading_day BOOLEAN               -- Crucial for Stock Markets!
);

-- 3. Create the Fact Table: Trades
CREATE TABLE fact_trades (
    trade_id SERIAL PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),       -- Link to Time
    company_sk INT REFERENCES dim_company(company_sk),-- Link to Company
    price DECIMAL(10, 2),                -- The Measurement
    volume INT,                          -- The Measurement
    turnover DECIMAL(15, 2),             -- The Measurement
    created_at TIMESTAMP DEFAULT NOW()
);