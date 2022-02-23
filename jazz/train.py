import numpy as np
from sklearn.linear_model import LinearRegression

from faker import Faker
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

MODEL_NAME = "HAPPINESS_PROPHET"

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment(MODEL_NAME + "_experiments")

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
with mlflow.start_run() as run:
    run = mlflow.active_run()
    lr = LinearRegression()
    lr.fit(X, y)
    print(run.info)
    result = mlflow.register_model(
        run.info.run_id,
        MODEL_NAME
    )
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=int(result.version),
        stage="Staging"
    )




