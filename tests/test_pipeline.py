from jazz.data import generate, generate_xml
from jazz.pipeline import to_bronze, to_silver, to_gold, parse_xml

from pyspark.sql import Row
from pyspark.sql.functions import col

def test_to_bronze(tmpdir, spark):
    path = str(tmpdir)
    raw_path = path + "/raw"
    generate(raw_path, 3)
    bronze_df = to_bronze(spark, raw_path)
    bronze_df.show()
    schema = bronze_df.schema.fieldNames()
    assert(len(schema) == 1)
    assert(schema[0] == "value")
    assert(bronze_df.count() == 3)


def test_to_silver(tmpdir, spark):
    path = str(tmpdir)
    raw_path = path + "/raw"
    generate(raw_path, 3)
    bronze_df = to_bronze(spark, raw_path)
    silver_df = to_silver(bronze_df)
    schema = silver_df.schema
    fields = schema.fieldNames()
    print(schema)
    print(fields)
    assert("value" in fields)
    assert("message" in fields)
    silver_df.show()


def test_to_gold(spark):
    df = spark.createDataFrame([
        Row(id = 1, text = "My name is Charlie Brown")
    ])
    new_df = to_gold(df, "id", "text")
    new_df.show()
    names = new_df.schema.fieldNames() 
    assert("id" in names)
    assert("entities" in names)
    assert("types" in names)

def test_parse_xml(spark):
    xml_string = generate_xml()
    df = spark.createDataFrame([
        Row(value = xml_string)
    ])
    df = df.select(parse_xml(col("value")).alias("message"))
    schema = df.schema
    fields = schema.fieldNames()
    df = df.select("message.subject", "message.body")
    fields = df.schema.fieldNames()
    assert("subject" in fields)
    assert("body" in fields)
    values = df.collect()
    assert(len(values[0][0]) > 10)