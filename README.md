# ADX-python-logging
A python logging handler for Azure Data explorer

[![PyPI version](https://badge.fury.io/py/adx-python-logging.svg)](https://pypi.org/project/adx-python-logging/)

## Introduction

This package provides a Python logging handler for Azure Data Explorer (ADX). It allows you to send your application logs directly to an ADX cluster.

## Getting Started

### Prerequisites

Before you can use this package, you need to set up your environment variables. Create a `.env` file in your project root and add the following variables:

```
ADX_CLUSTER_URI=""
ADX_CLUSTER_INGESTION_URI=""
ADX_DATABASE_NAME=""
ADX_HANDLER_LEVEL="INFO"
LOG_TABLE_NAME="Log"
LOG_TABLE_MAPPING_NAME="Log_Mapping"
CLIENT_ID=""
CLIENT_SECRET=""
TENANT_ID=""
```
Replace the empty strings with your actual values.

### Setting up ADX

You also need to create a table and a JSON mapping in your ADX cluster. You can do this with the following Kusto Query Language (KQL) commands:
```kql
.create table my_table (timestamp: datetime, logger: string, level: string, message: string, thread_id: string, category: string, user: string)

.create table my_table ingestion json mapping 'my_table_mapping' '[{"column":"timestamp", "path":"$.asctime", "datatype":"datetime"}, {"column":"logger", "path":"$.name", "datatype":"string"}, {"column":"level", "path":"$.levelname", "datatype":"string"}, {"column":"message", "path":"$.message", "datatype":"string"}, {"column":"thread_id", "path":"$.thread", "datatype":"string"}, {"column":"category", "path":"$.category", "datatype":"string"}, {"column":"user", "path":"$.user", "datatype":"string"}]'
```

### Installation

You can install this package with pip:
```
pip install adx-python-logging
```

### Usage

Here is an example of how to use this package in your Python code:
```python
import logging
from dotenv import load_dotenv
from adx-python-logging import add_ADX_handler_to_logger

def log_str_func(record: logging.LogRecord):
    asctime_obj = datetime.datetime.utcfromtimestamp(record.created)
    formatted_asctime_str = asctime_obj.strftime("%Y-%m-%dT%H:%M:%S")
    json_str = json.dumps({
        "timestamp": formatted_asctime_str,
        "name": record.name,
        "level": record.levelname,
        "message": record.getMessage(),
        "thread": record.thread,
        "category": getattr(record, "category", None),
        "user": getattr(record, "user", None),
    })
    return json_str

load_dotenv()
logger = logging.getLogger("MyLogger")
add_ADX_handler_to_logger(logger, log_str_func)
logger.info("this is a info message.", extra={"category": "Test", "user": "BOT"})
```
This will send a log message to your ADX cluster whenever you call logger.info().

License
This project is licensed under the MIT License.