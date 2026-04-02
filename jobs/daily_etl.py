from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

# Initialize Spark session
spark = SparkSession.builder \
    .appName("SchemaAdjustmentJob") \
    .getOrCreate()

# Assuming df is the DataFrame read from Kafka
# Read the data
df = spark.read.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "incoming_topic") \
    .load()

# Assuming initial columns were: (user_id, transaction_amount, created_at, customer_segment)
# Check and transform the DataFrame to match the expected schema
# We need 'user_id', 'transaction_amount', and 'user_age'

# Add a new column 'user_age' with a default value, e.g., -1, as it's missing
df_transformed = df.withColumn("user_age", lit(-1))

# Select the required columns for downstream processing
df_result = df_transformed.select("user_id", "transaction_amount", "user_age")

# Show result or perform further processing
df_result.show()

# Stop Spark session
spark.stop()