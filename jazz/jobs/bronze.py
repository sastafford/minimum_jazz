import sys
from argparse import ArgumentParser

from jazz.data import generate
from jazz.pipeline import to_bronze
from jazz.helper import get_spark

p = ArgumentParser()
p.add_argument("--number_files", required=False, type=int, default=100)
p.add_argument("--xml_directory", required=False, type=str, default="/tmp/minimum_jazz/raw")
p.add_argument("--project_home", required=False, type=str, default="/dbfs/Shared/minimum_jazz/")
namespace = p.parse_known_args(sys.argv[1:])[0]

generate(namespace.xml_directory, namespace.number_files)

raw_dir = namespace.project_home + "/raw"
bronze_dir = namespace.project_home + "/bronze"
df = to_bronze(get_spark(), raw_dir)
print(bronze_dir)
df.write.format("delta").save(bronze_dir)