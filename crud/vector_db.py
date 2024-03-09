from langchain_community.vectorstores import Qdrant
from utils.azure import get_azure_open_ai_embeddings
from qdrant_client import QdrantClient

from config import settings


QDRANT_URL = f"http://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}"
QDRANT_CLIENT = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

AZURE_EMBEDDINGS = get_azure_open_ai_embeddings()


def create_document_vector(file):
    file_content =file.file.read()
    Qdrant.from_texts([file_content.decode('utf-8')], AZURE_EMBEDDINGS, url=QDRANT_URL, collection_name=file.filename)


def read_document_vector(document_name):
    
    return Qdrant(client=QDRANT_CLIENT, collection_name=document_name, embeddings=AZURE_EMBEDDINGS)
