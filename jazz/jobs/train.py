import numpy as np
import os
import sys
from sklearn.linear_model import LinearRegression
from argparse import ArgumentParser

from faker import Faker
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

mlflow_tracking_uri = os.environ['MLFLOW_TRACKING_URI']
MODEL_NAME = "happiness_prophet"
experiment_name = "/Shared/dbx/projects/" + MODEL_NAME

p = ArgumentParser()
p.add_argument("--mlflow_tracking_uri", required=False, type=str, default=mlflow_tracking_uri)
p.add_argument("--experiment", required=False, type=str, default=experiment_name)
namespace = p.parse_known_args(sys.argv[1:])[0]

mlflow.set_tracking_uri(namespace.mlflow_tracking_uri)
experiment = mlflow.get_experiment_by_name(namespace.experiment)

if (experiment is None):
    experiment_id = mlflow.create_experiment(namespace.experiment)
    experiment = mlflow.get_experiment(experiment_id)

SLOPE = Faker().random_int(0, 42)
INTERCEPT = Faker().random_int(0, 42)

def linear(x):
    return (SLOPE * x) + INTERCEPT + get_noise()

def get_noise() -> int:
    return Faker().pyfloat(min_value = -1.0, max_value = 1.0)


X = np.array([range(-10, 10)]).reshape(-1, 1)
y_values = []
for x in np.nditer(X):
    y_values.append(linear(x))
y = np.array(y_values) 

client = MlflowClient()
mlflow.sklearn.autolog()
with mlflow.start_run(experiment_id=experiment.experiment_id) as run:
    run = mlflow.active_run()
    lr = LinearRegression()
    lr.fit(X, y)
    print(run.info)
    result = mlflow.register_model(
        model_uri="runs:/" + run.info.run_id + "/model",
        name=MODEL_NAME
    ) #await_registration_for=300  use for mlflow later version
#    client.transition_model_version_stage(
#        name=MODEL_NAME,
#        version=int(result.version),
#        stage="Staging"
#    )