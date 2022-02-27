from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
import pytest
import os

@pytest.fixture(scope="session", autouse=True)
def spark() -> SparkSession:
    is_local = True if "SPARK_ENV_LOADED" not in os.environ.keys() else False
    if (is_local):
        builder = SparkSession.builder \
                .config(
                    "spark.sql.extensions", 
                    "io.delta.sql.DeltaSparkSessionExtension") \
                .config(
                    "spark.sql.catalog.spark_catalog", 
                    "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        spark = configure_spark_with_delta_pip(builder).getOrCreate()
    return spark
