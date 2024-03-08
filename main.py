from functools import lru_cache
from typing import Annotated

from fastapi import FastAPI, UploadFile, HTTPException, Depends, File 
from azure.storage.blob import BlobServiceClient
from sqlalchemy.orm import Session
from langchain.vectorstores import Qdrant
from langchain_openai import AzureOpenAIEmbeddings

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
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask", response_model=schemas.Answer)
def ask_question(ask_data: schemas.AskQuestion, db: Session = Depends(get_db)):
    try:
        question = ask_data.question
        document_name = ask_data.document_name

        fake_answer = "this fake answer"

        documwnt = service.get_documwnt_by_name(db, document_name)
    
        service.create_question_answer(db, documwnt.id, question, fake_answer)
    
        return {"question":question, "answer": fake_answer}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
