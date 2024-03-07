from functools import lru_cache
from typing import Annotated

from fastapi import FastAPI, UploadFile, HTTPException, Depends, File 
from azure.storage.blob import BlobServiceClient
from sqlalchemy.orm import Session

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
        service.create_file(db, file.filename)

        blob_service_client = BlobServiceClient.from_connection_string(settings.connection_string)

        blob_client = blob_service_client.get_blob_client(container=settings.container_name, blob=file.filename)

        blob_client.upload_blob(file.file)

        return {"filename": file.filename, "message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask", response_model=schemas.Answer)
def ask_question(question: schemas.Question, db: Session = Depends(get_db)):
    try:
        fake_answer = "this fake answer"
        return {"question":question, "answer": fake_answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
