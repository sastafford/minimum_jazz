from pyspark.sql import DataFrame
from typing import Dict
import xml.etree.ElementTree as ET

def to_bronze(spark, raw_path) -> DataFrame:
    df = spark.read.format("text").load(raw_path + "/*.xml")
    return df

def to_silver(spark, bronze_path) -> DataFrame:
    df = spark.read.format("delta").load(bronze_path)
    df = df.withColumnRenamed("value", "xml")
    #df.show()

def parse_xml(xml_string: str) -> Dict:
    values = {}
    root = ET.fromstring(xml_string)
    values["SUBJECT"] = root.findall(".//SUBJECT")[0].text
    return values
