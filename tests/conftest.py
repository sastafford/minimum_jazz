from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
import pytest

@pytest.fixture(scope="session", autouse=True)
def spark() -> SparkSession:
    builder = SparkSession.builder.appName("local-spark") \
        .config(
            "spark.sql.extensions", 
            "io.delta.sql.DeltaSparkSessionExtension") \
        .config(
            "spark.sql.catalog.spark_catalog", 
            "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    return spark