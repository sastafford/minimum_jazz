from setuptools import find_packages, setup

setup(
    name="minimum_jazz",
    #packages=find_packages(exclude=["tests", "tests.*"]),
    packages=find_packages(),
    setup_requires=["wheel"],
    version="0.1.0",
    description="Lakehouse Architecture data piplines examples",
    author="Scott Stafford"
)