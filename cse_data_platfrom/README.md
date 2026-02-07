# CSE Data Platform - Dockerized Data Engineering Environment

## Overview
This project sets up a comprehensive data engineering environment using Docker Compose. It integrates the following services:

*   **Airflow** (Orchestration): Scheduled DAGs and workflow management.
*   **Spark** (Data Processing): Distributed data processing (Master & Worker nodes).
*   **MinIO** (Data Lake): S3-compatible object storage.
*   **PostgreSQL** (Data Warehouse): Relational database for structured data.

## Project Structure
```bash
cse_data_platfrom/
├── dags/                  # Airflow DAGs (e.g., daily_cse_pipeline.py)
├── data/                  # Shared data volume between Host, Airflow, and Spark
├── scripts/               # Python scripts for extraction, loading, and processing
├── sql/                   # Database initialization scripts (init_airflow.sql)
└── docker-compose.yaml    # Docker service definitions
```

## Getting Started

### Prerequisites
- Docker & Docker Compose installed.

### Start Services
Run the following command in the project root:
```bash
docker-compose up -d
```

### Accessing Services

| Service | Architecture | URL / Connection | Credentials |
| :--- | :--- | :--- | :--- |
| **Airflow UI** | Web Interface | [http://localhost:8080](http://localhost:8080) | `admin` / `admin` |
| **Spark Master** | Web Interface | [http://localhost:9090](http://localhost:9090) | N/A |
| **MinIO Console** | Web Interface | [http://localhost:9001](http://localhost:9001) | `minio_admin` / `minio_password` |
| **MinIO API** | 53-API Endpoint | `localhost:9000` | Same as above |
| **Postgres (Warehouse)** | Database | `localhost:5433` | `user` / `Kavindu2002` |
| **Postgres (Airflow DB)** | Internal DB | `postgres:5432` | `airflow` / `airflow` |

> **Note on Ports:**
> - The local Postgres instance runs on port **5433** to avoid conflict with any existing local Postgres running on 5432.
> - Spark Master UI is mapped to **9090** (internal 8080) to avoid conflict with Airflow UI.

## Workflows & Usage

### 1. Generating Mock Data
You can generate a large dataset (1 Million rows) directly inside the Airflow container. The script saves the file to the shared `data/` volume.

```bash
docker exec cse_data_platfrom-airflow-1 python /opt/airflow/scripts/generate_big_data.py
```
*Output:* `data/historical_trades.csv`

### 2. Processing Data with Spark
Run a PySpark job to process the generated CSV file. This calculates average price and volume per stock and saves the result as Parquet.

**Using `spark-submit` inside the Spark Master container:**
```bash
docker exec spark_master /opt/spark/bin/spark-submit /opt/spark/data/process_historical_data.py
```
*Output:* `data/processed_report/` (Parquet files)

### 3. Airflow DAGs
The `daily_cse_pipeline` DAG orchestrates daily extraction and loading tasks.
- Go to [Airflow UI](http://localhost:8080).
- Unpause the DAG `cse_daily_trade_pipeline`.
- Trigger it manually or wait for the daily schedule.

## Troubleshooting & Verification

### Common Commands
- **Check Running Containers:**
  ```bash
  docker ps
  ```
- **Check Service Logs:**
  ```bash
  docker logs -f cse_data_platfrom-airflow-1
  docker logs -f spark_master
  ```
- **Access Postgres CLI:**
  ```bash
  docker exec -it cse_warehouse psql -U user -d cse_dwh
  ```

### Implementation Details & Fixes Applied
During setup, several key configurations were applied to ensure stability:

1.  **Port Conflict (5432)**:
    - Host port `5433` is mapped to container port `5432` for Postgres.
2.  **Airflow Database Initialization**:
    - A custom `init_airflow.sql` script initializes the `airflow` user and database.
    - Explicit `GRANT ALL ON SCHEMA public TO airflow;` is applied to fix permission errors during container startup.
3.  **Spark Image**:
    - Switched from `bitnami/spark` to `apache/spark:3.5.0` for better compatibility.
    - Configured correct `spark-submit` paths (`/opt/spark/bin/spark-submit`).
4.  **Shared Volumes**:
    - The local `./data` directory is mounted to `/opt/spark/data` in both Spark Master and Worker containers, allowing seamless file sharing between host and containers.
    - Scripts are mounted to `/opt/airflow/scripts` for Airflow access.

## Clean Up
To stop all services:
```bash
docker-compose down
```
To stop and remove volumes (reset data):
```bash
docker-compose down -v
```
