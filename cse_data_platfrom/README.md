# CSE Data Platform - Real-time & Batch Data Engineering Environment

## Overview
This project simulates a complete data engineering platform for the Colombo Stock Exchange (CSE). It combines batch processing (Airflow + Spark) and real-time streaming (Kafka + Go Producer).

**Core Components:**
*   **Airflow** (Orchestration): Manages daily batch workflows.
*   **Spark** (Data Processing): Distributed computing for large-scale data transformation.
*   **MinIO** (Data Lake): Object storage for raw and processed data.
*   **PostgreSQL** (Data Warehouse): Stores structured data for reporting.
*   **Kafka** (Event Streaming): Handles real-time trade data streams.
*   **Go Producer**: Simulates real-time market activity.

## Project Structure
```bash
cse_data_platfrom/
├── dags/                  # Airflow DAGs (daily_cse_pipeline.py)
├── data/                  # Shared data volume (Host <-> Airflow <-> Spark)
├── producer/              # Go-based Kafka Producer
│   ├── main.go            # Producer source code
│   └── go.mod             # Go module definition
├── scripts/               # Python scripts for ETL tasks
├── sql/                   # Database initialization scripts
└── docker-compose.yaml    # Docker service orchestration
```

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Go (Golang) 1.20+ (for the producer)

### 1. Start Services
Run the following command in the `cse_data_platfrom` directory:
```bash
docker-compose up -d
```

### 2. Service Access Points

| Service | URL / Connection | Credentials |
| :--- | :--- | :--- |
| **Airflow UI** | [http://localhost:8080](http://localhost:8080) | `admin` / `admin` |
| **Spark Master** | [http://localhost:9090](http://localhost:9090) | N/A |
| **MinIO Console** | [http://localhost:9001](http://localhost:9001) | `minio_admin` / `minio_password` |
| **Postgres (Warehouse)** | `localhost:5433` | `user` / `Kavindu2002` |
| **Kafka (Internal)** | `kafka:29092` | N/A |
| **Kafka (External)** | `localhost:9092` | N/A |

## Workflows

### Batch Processing (Historical Data)
1.  **Generate Data**: Execute the generator script inside the Airflow container.
    ```bash
    docker exec cse_data_platfrom-airflow-1 python /opt/airflow/scripts/generate_big_data.py
    ```
    *Creates `data/historical_trades.csv` (1M rows).*

2.  **Process with Spark**: Submit a PySpark job to calculate average metrics.
    ```bash
    docker exec spark_master /opt/spark/bin/spark-submit /opt/spark/data/process_historical_data.py
    ```
    *Saves results to `data/processed_report/` (Parquet).*

3.  **Automate with Airflow**:
    - Go to [Airflow UI](http://localhost:8080).
    - Unpause `cse_daily_trade_pipeline`.
    - Updates are scheduled daily.

### Real-Time Streaming
1.  **Initialize Kafka Topic**: Before running the producer, create the topic (run once):
    ```bash
    docker exec kafka kafka-topics --bootstrap-server kafka:29092 --create --topic cse_trades
    ```

2.  **Run the Go Producer**: simulates live trades being sent to Kafka.
    ```bash
    cd producer
    go run main.go
    ```
    *You should see output like: `Sent: JKH - 150.25`*

3.  **Run Spark Consumer**:
    ```bash
    docker exec -it spark_master /opt/spark/bin/spark-submit \
        --conf "spark.jars.ivy=/tmp/.ivy2" \
        --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
        /opt/spark/data/stream_processor.py
    ```

## Implementation Details & Fixes
- **Port Conflicts**: Remapped Postgres to host port `5433` to avoid local conflicts.
- **Airflow**: Added custom `init_airflow.sql` to handle database creation and permissions (`GRANT ALL ON SCHEMA public`).
- **Spark**: Switched to official `apache/spark:3.5.0` images due to Bitnami unavailability.
- **Volumes**: Mounted local `./data` directory to all Spark and Airflow containers for seamless file sharing.
- **Kafka**: Configured advertised listeners (`PLAINTEXT_HOST`) to allow connections from both Docker containers and your local machine (localhost).

## Troubleshooting
- **Producer Fails?** Ensure the topic `cse_trades` exists (use the command above).
- **Services Down?** Check logs: `docker logs cse_data_platfrom-airflow-1` or `docker logs kafka`.
- **Reset Environment**: `docker-compose down -v` (Running with `-v` deletes database volumes).
