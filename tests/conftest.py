from pyspark.sql import SparkSession
from jazz.helper import get_spark
import pytest


@pytest.fixture(scope="session", autouse=True)
def spark() -> SparkSession:
    return get_spark()
