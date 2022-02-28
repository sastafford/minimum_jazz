import sys
from argparse import ArgumentParser

from jazz.pipeline import to_silver
from jazz.helper import get_spark

p = ArgumentParser()
p.add_argument("--project_home", required=False, type=str, default="/dbfs/Shared/minimum_jazz/")
namespace = p.parse_known_args(sys.argv[1:])[0]

bronze_dir = namespace.project_home + "/bronze"
silver_dir = namespace.project_home + "/silver"

spark = get_spark()

bronze_df = spark.read.format("delta").load(bronze_dir)
silver_df = to_silver(bronze_df)
silver_df.write.format("delta").save(silver_dir)