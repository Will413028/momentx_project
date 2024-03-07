from functools import lru_cache
from typing import Annotated

from fastapi import FastAPI, UploadFile, HTTPException, Depends, File 
from azure.storage.blob import BlobServiceClient

from config import Settings

app = FastAPI()

@lru_cache
def get_settings():
    return Settings()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/uploadfile")
def create_upload_file(settings: Annotated[Settings, Depends(get_settings)], file: UploadFile = File(...)):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(settings.connection_string)

        blob_client = blob_service_client.get_blob_client(container=settings.container_name, blob=file.filename)

        blob_client.upload_blob(file.file)
        return {"filename": file.filename, "message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
