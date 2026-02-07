from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, window

def process_data():
    # 1. Initialize Spark Session
    # We need to download the AWS S3 JARs automatically to talk to MinIO
    spark = SparkSession.builder \
        .appName("CSE_Historical_Processor") \
        .master("spark://spark-master:7077") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4") \
        .getOrCreate()

    # 2. Read CSV (Lazy Evaluation - nothing happens yet)
    # Note: In a real cluster, the file must be accessible to all workers (e.g., in S3/MinIO)
    # For this local demo, we will mount the data folder to the spark worker in docker-compose
    df = spark.read.csv("/opt/spark/data/historical_trades.csv", header=True, inferSchema=True)

    # 3. Transformation: Calculate Average Price per Stock
    print("Processing data...")
    report_df = df.groupBy("symbol").agg(
        avg("price").alias("avg_price"),
        avg("volume").alias("avg_volume")
    )

    # 4. Action: Show results (This triggers the computation)
    report_df.show()

    # 5. Write to Parquet (Simulating Data Lake storage)
    # In a real job, we would write this to "s3a://cse-lake/processed/"
    report_df.write.mode("overwrite").parquet("/opt/spark/data/processed_report")
    
    print("Processing Complete. Saved to Parquet.")
    spark.stop()

if __name__ == "__main__":
    process_data()