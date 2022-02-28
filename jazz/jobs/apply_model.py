import mlflow
from mlflow.tracking import MlflowClient

import sys
import os
from argparse import ArgumentParser

mlflow_tracking_uri = os.environ['MLFLOW_TRACKING_URI']

p = ArgumentParser()
p.add_argument("--mlflow_tracking_uri", required=False, type=str, default=mlflow_tracking_uri)
p.add_argument("--model_name", required=True, type=str)
namespace = p.parse_known_args(sys.argv[1:])[0]

MODEL_NAME = namespace.model_name
mlflow.set_tracking_uri(namespace.mlflow_tracking_uri)

def _get_model_from_registry(run_id: str):
    model_uri = "runs:/{}/model".format(run_id)
    print(model_uri)
    model = mlflow.sklearn.load_model(model_uri)
    return model

client = MlflowClient()
versions = client.get_latest_versions(MODEL_NAME)
run_id = versions[0].run_id

model = _get_model_from_registry(run_id)
print(type(model))
print(model.predict([[-10], [-9], [-8], [-7], [-6]]))