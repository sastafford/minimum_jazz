from pyspark.sql import DataFrame

def to_bronze(spark, raw_path) -> DataFrame:
    df = spark.read.format("text").load(raw_path + "/*.xml")
    return df

def to_silver(spark, bronze_path) -> DataFrame:
    df = spark.read.format("delta").load(bronze_path)
    df = df.withColumnRenamed("value", "xml")
    df.show()