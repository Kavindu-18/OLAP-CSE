from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, sum as _sum
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

def start_streaming():
    # 1. Initialize Spark with Kafka Dependencies
    spark = SparkSession.builder \
        .appName("CSE_RealTime_Analytics") \
        .master("spark://spark-master:7077") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .getOrCreate()

    # Disable noisy logging
    spark.sparkContext.setLogLevel("WARN")

    # 2. Define the Schema (Must match your Go struct!)
    # Go sends: {"symbol":"JKH", "price":150.0, "volume":100, "timestamp":"..."}
    schema = StructType([
        StructField("symbol", StringType(), True),
        StructField("price", DoubleType(), True),
        StructField("volume", IntegerType(), True),
        StructField("timestamp", StringType(), True)
    ])

    # 3. Read Stream from Kafka
    # "kafka:9092" is the internal Docker hostname for Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "cse_trades") \
        .option("startingOffsets", "latest") \
        .load()

    # 4. Parse JSON
    # Kafka sends data in a binary 'value' column. We cast to String then parse to JSON.
    parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

    # 5. Process: Calculate Total Volume by Stock
    # This is the "Business Logic"
    market_summary = parsed_df.groupBy("symbol").agg(
        _sum("volume").alias("total_volume")
    )

    # 6. Output: Write to Console
    # 'outputMode("complete")' means: "Show me the WHOLE table every time it updates"
    query = market_summary.writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

    print("Streaming started... Waiting for trades...")
    query.awaitTermination()

if __name__ == "__main__":
    start_streaming()