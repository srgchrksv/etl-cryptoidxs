from azure.storage.blob import BlobServiceClient

def storage_connection(storage_account_name, storage_account_key, container_name):
    storage_connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(
    storage_connection_string
)
    container_client = blob_service_client.get_container_client(container_name)
    return container_client

