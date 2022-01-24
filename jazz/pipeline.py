from pyspark.sql import DataFrame
from pyspark.sql.functions import udf, col

from typing import Dict
import xml.etree.ElementTree as ET

def to_bronze(spark, raw_path: str) -> DataFrame:
    df = spark.read.format("text").load(raw_path + "/*.xml")
    return df

def to_silver(spark, bronze_df: DataFrame) -> DataFrame:
    parseXml = udf(parse_xml)
    df = bronze_df.select("value", parseXml(col("value")))
    return df

def parse_xml(xml_string: str) -> Dict:
    values = {}
    root = ET.fromstring(xml_string)
    values["SUBJECT"] = root.findall(".//SUBJECT")[0].text
    return values
