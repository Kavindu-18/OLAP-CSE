from pyspark.sql.functions import lit

def apply_schema_healing(df):
    """
    Auto-Healer generated fix:
    The column 'user_age' was missing and replaced by 'customer_segment' upstream.
    Recreating 'user_age' with a null integer to stabilize downstream pipelines.
    """
    if "user_age" not in df.columns and "customer_segment" in df.columns:
        df = df.withColumn("user_age", lit(None).cast("integer")) 
    return df
