from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

import db.models as models


def create_file(db: Session, file_name: str):

    try:    
        db_document = models.Document(name=file_name)

        db.add(db_document)
        db.commit()
        db.refresh(db_document)
    except Exception as e:
        db.rollback()

        error_message = str(e)
        print(error_message)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'File create failed: {error_message}'
        )


def get_documwnt_by_name(db: Session, name: str) -> models.Document:
    query = select(models.Document).where(models.Document.name == name)
    document = db.execute(query).scalar()

    return document


def create_question_answer(db: Session, document_id: int, question: str, answer: str):
    try:
        db_question_answer = models.QuestionAnswer(document_id=document_id, question=question, answer=answer)

        db.add(db_question_answer)
        db.commit()
        db.refresh(db_question_answer)
    except Exception as e:
        db.rollback()

        error_message = str(e)
        print(error_message)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Question Answer create failed: {error_message}'
        )
