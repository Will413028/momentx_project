from fastapi import FastAPI, UploadFile, HTTPException, Depends, File, status
from sqlalchemy.orm import Session
from langchain_community.vectorstores import Qdrant
from langchain.chains import ConversationalRetrievalChain
from qdrant_client import QdrantClient

import service
import schemas
from config import settings
from db.database import get_db
from utils.azure import get_azure_open_ai_embeddings, get_azure_chat_open_ai, upload_file_azure_blob

QDRANT_URL = f"http://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}"
QDRANT_CLIENT = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

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
        
        Qdrant.from_texts([file_content.decode('utf-8')], embeddings, url=QDRANT_URL, collection_name=file.filename)

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

        embeddings = get_azure_open_ai_embeddings()

        qdrant = Qdrant(client=QDRANT_CLIENT, collection_name=document_name, embeddings=embeddings)

        azure_chat = get_azure_chat_open_ai()

        qa = ConversationalRetrievalChain.from_llm(llm=azure_chat, retriever=qdrant.as_retriever())

        result = qa({"question": question, 'chat_history': []})

        answer = result['answer']

        documwnt = service.get_documwnt_by_name(db, document_name)

        service.create_question_answer(db, documwnt.id, question, answer)

        return {"question":question, "answer": answer}

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
