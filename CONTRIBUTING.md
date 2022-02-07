# Welcome to Stretchy contributing guide

## Prerequisites

### Local Development

 * Python 3.9
 * [pipenv](https://pipenv.pypa.io/en/latest/) to help facilitate local development 

### Continuous Integration Toolset
 
 * [pytest](https://docs.pytest.org/) is a framework for writing tests
 * [Setup Tools](https://setuptools.pypa.io/en/latest)

## Local Environment Setup

Install a virtual environment from Pipfile.  The --dev option will install the dev packages, the -e option allows to develop locally without building libraries. 

```python
pipenv install --dev -e .
```

## Run tests locally

```
pytest
```

## Build Python whl

The whl file is placed under the ./dist folder.

```python
python setup.py clean build bdist_wheel
```
