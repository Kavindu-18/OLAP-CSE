-- Create the airflow user
CREATE USER airflow WITH PASSWORD 'airflow';

-- Create the airflow database
CREATE DATABASE airflow;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;

-- Grant schema privileges (Crucial for Airflow to create tables)
\connect airflow
GRANT ALL ON SCHEMA public TO airflow;
