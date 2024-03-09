from fastapi import FastAPI, UploadFile, HTTPException, Depends, File, status
from sqlalchemy.orm import Session

import schemas
import crud.sql_db
import crud.vector_db
from db.database import get_db
from utils.azure import upload_file_azure_blob, generate_question_response


app = FastAPI()


@app.get("/test")
def test_server():
    return {"Test"}


@app.post("/uploadfile")
def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        upload_file_azure_blob(file)

        file.file.seek(0)

        crud.vector_db.create_document_vector(file)
        crud.sql_db.create_file(db, file.filename)

        return {"filename": file.filename, "message": "File uploaded successfully"}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/ask", response_model=schemas.Answer)
def ask_question(ask_data: schemas.AskQuestion, db: Session = Depends(get_db)):
    try:
        question = ask_data.question
        document_name = ask_data.document_name

        document_vector = crud.vector_db.read_document_vector(document_name)

        result = generate_question_response(question, document_vector)

        answer = result['answer']

        crud.sql_db.create_question_answer_of_document(db, document_name, question, answer)

        return {"question":question, "answer": answer}

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
