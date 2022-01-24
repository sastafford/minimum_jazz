from pyspark.sql import DataFrame

def to_bronze(spark, raw_path) -> DataFrame:
    df = spark.read.format("text").load(raw_path + "/*.xml")
    return df

