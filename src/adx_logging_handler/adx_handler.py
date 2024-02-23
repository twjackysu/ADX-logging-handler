from azure.kusto.data import DataFormat
from azure.kusto.ingest import QueuedIngestClient, IngestionProperties, StreamDescriptor
import logging
import os
import io
import uuid
from src.adx_logging.ingest_client import get_ingest_client


def add_ADX_handler_to_logger(
    logger: logging.Logger, get_log_str: callable[[logging.LogRecord], str]
):
    database_name = os.getenv("ADX_DATABASE_NAME")
    table_name = os.getenv("LOG_TABLE_NAME")
    mapping_name = os.getenv("LOG_TABLE_MAPPING_NAME")

    ingestion_props = IngestionProperties(
        database=database_name,
        table=table_name,
        data_format=DataFormat.JSON,
        ingestion_mapping_reference=mapping_name,
    )

    ingest_client = get_ingest_client()

    class ADXHandler(logging.Handler):
        def emit(self, record):
            send_logs_to_adx_queue(record, ingest_client, ingestion_props, get_log_str)

    adx_handler = ADXHandler()
    adx_handler_level = os.getenv("ADX_HANDLER_LEVEL", "INFO")
    # Set the level of the ADX handler to INFO or above
    adx_handler.setLevel(adx_handler_level)

    logger.addHandler(adx_handler)


def generate_stream_from_string(s: str):
    stream = io.BytesIO()
    stream.write(s.encode("utf-8"))
    stream.seek(0)
    return stream


# Send log data to the Azure Data Explorer queue
def send_logs_to_adx_queue(
    record: logging.LogRecord,
    ingest_client: QueuedIngestClient,
    ingestion_props: IngestionProperties,
    get_log_str: callable[[logging.LogRecord], str],
):
    source_id = str(uuid.uuid4())
    try:
        json_str = get_log_str(record)
        # Use the client to send log data to Azure Data Explorer
        stream_descriptor = StreamDescriptor(
            generate_stream_from_string(json_str), source_id=source_id
        )
        ingest_client.ingest_from_stream(
            stream_descriptor, ingestion_properties=ingestion_props
        )

    except Exception as e:
        print(f"Failed to send logs to ADX: {e}. source_id: {source_id}")
