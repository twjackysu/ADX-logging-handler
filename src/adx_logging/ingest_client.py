from azure.kusto.data import KustoConnectionStringBuilder
from azure.kusto.ingest import QueuedIngestClient
import os

client = None


def get_ingest_client():
    global client

    if client is not None:
        return client

    ingest_connection = (
        KustoConnectionStringBuilder.with_aad_application_key_authentication(
            os.getenv("ADX_CLUSTER_INGESTION_URI"),
            os.getenv("CLIENT_ID"),
            os.getenv("CLIENT_SECRET"),
            os.getenv("TENANT_ID"),
        )
    )

    ingest_client = QueuedIngestClient(ingest_connection)

    return ingest_client
