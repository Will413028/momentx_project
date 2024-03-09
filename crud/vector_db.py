from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from langchain.text_splitter import  RecursiveCharacterTextSplitter

from config import settings
from utils.azure import get_azure_open_ai_embeddings


QDRANT_URL = f"http://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}"
QDRANT_CLIENT = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
AZURE_EMBEDDINGS = get_azure_open_ai_embeddings()


def create_document_vector(file):
    file_content =file.file.read()

    file_string = file_content.decode('utf-8')

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap  = 50,
        )

    texts = text_splitter.split_text(file_string)

    Qdrant.from_texts(texts, AZURE_EMBEDDINGS, url=QDRANT_URL, collection_name=file.filename)


def read_vectors_by_document_name(document_name):
    
    return Qdrant(client=QDRANT_CLIENT, collection_name=document_name, embeddings=AZURE_EMBEDDINGS)
