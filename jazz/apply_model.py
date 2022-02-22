import mlflow

def _get_model_from_registry(model_name: str, stage: str):
    model_uri = "models:/{}/{}".format(model_name, stage)
    print(model_uri)
    model = mlflow.sklearn.load_model(model_uri=model_uri)
    return model

mlflow.set_tracking_uri("http://127.0.0.1:5000")
model = _get_model_from_registry("log-regression", "Production")
print(type(model))