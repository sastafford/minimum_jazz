from pyspark.sql import DataFrame
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StructField, StructType, StringType, MapType

from typing import Dict
import xml.etree.ElementTree as ET

def to_bronze(spark, raw_path: str) -> DataFrame:
    df = spark.read.format("text").load(raw_path + "/*.xml")
    return df

def to_silver(spark, bronze_df: DataFrame) -> DataFrame:
    df = bronze_df.select("value", parse_xml(col("value")).alias("message"))
    return df

def _parse_xml_struct_schema():
    return StructType([
            StructField('subject', StringType(), nullable=True),
            StructField('body', StringType(), nullable=True)
        ])

@udf(returnType=_parse_xml_struct_schema())
def parse_xml(xml_string: str) -> Dict:
    values = {}
    root = ET.fromstring(xml_string)
    values["subject"] = root.findall(".//SUBJECT")[0].text
    values["body"] = root.findall(".//BODY")[0].text
    return values
