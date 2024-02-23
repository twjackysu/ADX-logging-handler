from setuptools import setup, find_packages

setup(
    name="adx-logging-handler",
    version="1.0.1",
    description="A python logging handler for Azure Data explorer",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["azure-kusto-data", "azure-kusto-ingest"],
)
