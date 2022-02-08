import pandas as pd
from pyspark.sql import DataFrame
from pyspark.sql.functions import udf, col, pandas_udf, size, explode, lit
from pyspark.sql.types import StructField, StructType, StringType

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

from typing import Dict
import xml.etree.ElementTree as ET

def to_bronze(spark, raw_path: str) -> DataFrame:
    df = spark.read.format("text").load(raw_path + "/*.xml")
    return df

def to_silver(bronze_df: DataFrame) -> DataFrame:
    df = bronze_df.select("value", parse_xml(col("value")).alias("message"))
    return df

def to_gold(silver_df: DataFrame, id_col: str, text_col: str) -> DataFrame:
    """function that finds all named entities in a column of text in a Spark dataframe and returns the entities along with their types

    Parameters:
    - silver_df: a Spark dataframe with at least one column of clean text
    - id_col: a column in silver_df that uniquely identifies the row from which each entity was derived
    - text_col: a column in silver_df that contains the text containing the entities to extract

    Returns:
    - a Spark dataframe with three columns: the ID, the entities, and the entity types
    """

    get_ner_with_transformers_udf = pandas_udf(_get_ner_with_transformers, returnType=ArrayType(ArrayType(StringType()), containsNull=True))

    df_with_ents = df.select(id_col, text_col, get_ner_with_transformers_udf(col(text_col)).alias("NER"))\
      .filter(size(col("NER")) > lit(0))\
      .drop(text_col)\
      .withColumn("NER", explode(col("NER")))\
      .withColumn("entity", col("NER")[1])\
      .withColumn("entity_type", col("NER")[0])\
      .drop("NER")
    
    return df_with_ents

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

def _get_ner_with_transformers(text_col: pd.Series) -> pd.Series:
    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER", padding=True)
    model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
    nlp = pipeline("ner", model=model, tokenizer=tokenizer)
    text_ner = nlp(text_col.values.tolist())
    ner_extracted = list(map(_extract_entities, text_ner))
    return pd.Series(ner_extracted)
    
  
def _extract_entities(ner_list):
    if len(ner_list) > 0:
      return [(e["entity"], e["word"]) for e in ner_list]
    else:
      return []

