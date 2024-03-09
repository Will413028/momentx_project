from functools import lru_cache
from typing import Annotated

from fastapi import FastAPI, UploadFile, HTTPException, Depends, File, status
from azure.storage.blob import BlobServiceClient
from sqlalchemy.orm import Session
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_openai import AzureChatOpenAI
from langchain.chains import ConversationalRetrievalChain

from config import Settings
import service
from db.database import get_db
import schemas


app = FastAPI()


@lru_cache
def get_settings():
    return Settings()


@app.get("/test")
def test_server():
    return {"Test"}


@app.post("/uploadfile")
def create_upload_file(settings: Annotated[Settings, Depends(get_settings)], file: UploadFile = File(...), db: Session = Depends(get_db), ):
    try:
        file_content = file.file.read()

        file.file.seek(0)

        embeddings = AzureOpenAIEmbeddings(
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=settings.AZURE_ENDPOINT,
            azure_deployment=settings.AZURE_EMBEDDING_MODEL_NAME,
            openai_api_version="2023-05-15",
        )

        Qdrant.from_texts([file_content.decode('utf-8')], embeddings, url=settings.QDRANT_URL, collection_name=settings.QDRANT_COLLECTION_NAME)

        service.create_file(db, file.filename)

        blob_service_client = BlobServiceClient.from_connection_string(settings.connection_string)

        blob_client = blob_service_client.get_blob_client(container=settings.container_name, blob=file.filename)

        blob_client.upload_blob(file.file)

        return {"filename": file.filename, "message": "File uploaded successfully"}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/ask", response_model=schemas.Answer)
def ask_question(settings: Annotated[Settings, Depends(get_settings)], ask_data: schemas.AskQuestion, db: Session = Depends(get_db)):
    try:
        question = ask_data.question
        document_name = ask_data.document_name

        blob_service_client = BlobServiceClient.from_connection_string(settings.connection_string)

        blob_client = blob_service_client.get_blob_client(container=settings.container_name, blob=document_name)

        stream = blob_client.download_blob()

        data = stream.readall()

        txt_content = data.decode("utf-8")

        embeddings = AzureOpenAIEmbeddings(
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=settings.AZURE_ENDPOINT,
            azure_deployment=settings.AZURE_EMBEDDING_MODEL_NAME,
            openai_api_version="2023-05-15",
            )

        vector_store = Qdrant.from_texts([txt_content], embeddings, location=":memory:", collection_name=settings.QDRANT_COLLECTION_NAME)

        azure_chat = AzureChatOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=settings.AZURE_ENDPOINT,
            azure_deployment=settings.AZURE_CHAT_MODEL_NAME,
            openai_api_version="2023-05-15",
            )

        qa = ConversationalRetrievalChain.from_llm(llm=azure_chat, retriever=vector_store.as_retriever())

        result = qa({"question": question, 'chat_history': []})

        answer = result['answer']

        documwnt = service.get_documwnt_by_name(db, document_name)

        service.create_question_answer(db, documwnt.id, question, answer)

        return {"question":question, "answer": answer}

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
