import mlflow
from mlflow.tracking import MlflowClient

def _get_model_from_registry(run_id: str):
    model_uri = "runs:/{}/model".format(run_id)
    print(model_uri)
    model = mlflow.sklearn.load_model(model_uri)
    return model

MODEL_NAME = "HAPPINESS_PROPHET"
mlflow.set_tracking_uri("http://127.0.0.1:5000")

client = MlflowClient()
versions = client.get_latest_versions(MODEL_NAME)
run_id = versions[0].run_id

model = _get_model_from_registry(run_id)
print(type(model))
print(model.predict([[-10], [-9], [-8], [-7], [-6]]))