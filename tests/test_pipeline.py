from jazz.data import generate
from jazz.pipeline import to_bronze

from pathlib import Path

def test_to_bronze(tmpdir, spark):
    generate(str(tmpdir), 3)
    bronze_df = to_bronze(spark, str(tmpdir))
    bronze_df.show()
    schema = bronze_df.schema.fieldNames()
    assert(len(schema) == 1)
    assert(schema[0] == "value")
    assert(bronze_df.count() == 3)

