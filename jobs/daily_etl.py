from pyspark.sql import SparkSession
from pyspark.sql.functions import col

df = df.withColumnRenamed("customer_segment", "user_age")