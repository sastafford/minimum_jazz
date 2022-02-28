from pyspark.sql import SparkSession
import os

is_local = True if "SPARK_ENV_LOADED" not in os.environ.keys() else False

if (is_local):
    from delta import configure_spark_with_delta_pip

def get_spark() -> SparkSession:
    if (is_local):
        builder = SparkSession.builder \
                .config(
                    "spark.sql.extensions", 
                    "io.delta.sql.DeltaSparkSessionExtension") \
                .config(
                    "spark.sql.catalog.spark_catalog", 
                    "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        spark = configure_spark_with_delta_pip(builder).getOrCreate()
    else:
        spark = SparkSession.builder.getOrCreate()
    return spark