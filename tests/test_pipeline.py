from jazz.data import generate, generate_xml
from jazz.pipeline import to_bronze, to_silver, parse_xml

from pathlib import Path

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
    bronze_path = path + "/bronze"
    bronze_df.write.format("delta").save(bronze_path)
    to_silver(spark, bronze_path)


def test_parse_xml():
    xml_string = generate_xml()
    values = parse_xml(xml_string)
    print(values)
    subject = values.get("SUBJECT")
    assert(len(subject) > 10)