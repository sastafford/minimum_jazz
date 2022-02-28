# Welcome to Stretchy contributing guide

## Prerequisites

### Local Development

* Python 3.9
* [pipenv](https://pipenv.pypa.io/en/latest/) to help facilitate local development
* mlflow 1.10.0
* Databricks Runtime 7.3 ML

### Continuous Integration Toolset

* [pytest](https://docs.pytest.org/) is a framework for writing tests
* [Setup Tools](https://setuptools.pypa.io/en/latest)

### Importing Natural Language Processing Libraries

Modern neural network-based NLP libraries such as Transformers can be very large and often don't fit in standard GitHub repos. To make them available to the package, download the necessary model files into the local repository's `data/` folder.

The default model in this package used for Named Entity Recognition (NER) is `bert-base-NER` from [Huggingface Hub](https://huggingface.co/dslim/bert-base-NER/tree/main). To make that model loadable from the local development environment, download the following artifacts:

* for the tokenizer:
  * `added_tokens.json`
  * `special_tokens_map.json`
  * `tokenizer_config.json`
  * `vocab.txt`
* for the model:
  * `config.json`
  * one of `flax_model.msgpack` (Flax), `pytorch_model.bin` (PyTorch) or `tf_model.h5` (TensorFlow) - whichever deep learning library you are working with.

The default location for these artifacts is `data/bert-base-ner`. If a different path is used, be sure to set the `model_path` argument to that path when calling `jazz.pipeline.to_gold()`.

## Local Environment Setup

Install a virtual environment from Pipfile.  The --dev option will install the dev packages, the -e option allows to develop locally without building libraries.

```python
pipenv install --dev -e .
```

## Run tests locally

```
pytest
```

## Run tests in Databrickss

```
dbx execute --cluster-name=<all_purpose_cluster_name> --job=minimum_jazz_test
```

## Build Python whl

The whl file is placed under the ./dist folder.

```python
python setup.py clean build bdist_wheel
```
