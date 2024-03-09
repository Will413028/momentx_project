from azure.storage.blob import BlobServiceClient
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import AzureChatOpenAI

from config import settings


def get_azure_open_ai_embeddings():

    return AzureOpenAIEmbeddings(
        api_key=settings.AZURE_OPENAI_API_KEY,
        azure_endpoint=settings.AZURE_ENDPOINT,
        azure_deployment=settings.AZURE_EMBEDDING_MODEL_NAME,
        openai_api_version="2023-05-15",
    )


def get_azure_chat_open_ai():

    return AzureChatOpenAI(
        api_key=settings.AZURE_OPENAI_API_KEY,
        azure_endpoint=settings.AZURE_ENDPOINT,
        azure_deployment=settings.AZURE_CHAT_MODEL_NAME,
        openai_api_version="2023-05-15",
    )


def upload_file_azure_blob(file):
    blob_service_client = BlobServiceClient.from_connection_string(settings.connection_string)
    blob_client = blob_service_client.get_blob_client(container=settings.container_name, blob=file.filename)
    blob_client.upload_blob(file.file)


def download_file_azure_blob(filename):
    blob_service_client = BlobServiceClient.from_connection_string(settings.connection_string)
    blob_client = blob_service_client.get_blob_client(container=settings.container_name, blob=filename)
    
    stream = blob_client.download_blob()
    data = stream.readall()

    return data.decode("utf-8")