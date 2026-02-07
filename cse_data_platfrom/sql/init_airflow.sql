-- Create the airflow user
CREATE USER airflow WITH PASSWORD 'airflow';

-- Create the airflow database
CREATE DATABASE airflow;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
