from fastapi import FastAPI, UploadFile, HTTPException, Depends, File, status
from sqlalchemy.orm import Session
from langchain_community.vectorstores import Qdrant
from langchain.chains import ConversationalRetrievalChain
from azure.storage.blob import BlobServiceClient

from config import settings
import service
from db.database import get_db
import schemas
from utils.azure import get_azure_open_ai_embeddings, get_azure_chat_open_ai, upload_file_azure_blob

app = FastAPI()


@app.get("/test")
def test_server():
    return {"Test"}


@app.post("/uploadfile")
def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        upload_file_azure_blob(file)

        file.file.seek(0)

        file_content = file.file.read()

        embeddings = get_azure_open_ai_embeddings()

        Qdrant.from_texts([file_content.decode('utf-8')], embeddings, url=settings.QDRANT_URL, collection_name=settings.QDRANT_COLLECTION_NAME)

        service.create_file(db, file.filename)

        return {"filename": file.filename, "message": "File uploaded successfully"}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/ask", response_model=schemas.Answer)
def ask_question(ask_data: schemas.AskQuestion, db: Session = Depends(get_db)):
    try:
        question = ask_data.question
        document_name = ask_data.document_name

        blob_service_client = BlobServiceClient.from_connection_string(settings.connection_string)

        blob_client = blob_service_client.get_blob_client(container=settings.container_name, blob=document_name)

        stream = blob_client.download_blob()

        data = stream.readall()

        txt_content = data.decode("utf-8")

        embeddings = get_azure_open_ai_embeddings()

        vector_store = Qdrant.from_texts([txt_content], embeddings, location=":memory:", collection_name=settings.QDRANT_COLLECTION_NAME)

        azure_chat = get_azure_chat_open_ai()

        qa = ConversationalRetrievalChain.from_llm(llm=azure_chat, retriever=vector_store.as_retriever())

        result = qa({"question": question, 'chat_history': []})

        answer = result['answer']

        documwnt = service.get_documwnt_by_name(db, document_name)

        service.create_question_answer(db, documwnt.id, question, answer)

        return {"question":question, "answer": answer}

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
