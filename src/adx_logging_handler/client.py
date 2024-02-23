from azure.kusto.data import KustoConnectionStringBuilder, KustoClient
import os

client = None


def get_client():
    global client

    if client is not None:
        return client

    connection = KustoConnectionStringBuilder.with_aad_application_key_authentication(
        os.getenv("ADX_CLUSTER_URI"),
        os.getenv("CLIENT_ID"),
        os.getenv("CLIENT_SECRET"),
        os.getenv("TENANT_ID"),
    )
    client = KustoClient(connection)

    return client
