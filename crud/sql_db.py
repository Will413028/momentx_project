from sqlalchemy import select
from sqlalchemy.orm import Session

import db.models as models


def create_file(db: Session, file_name: str):

    try:    
        db_document = models.Document(name=file_name)

        db.add(db_document)
        db.commit()
        db.refresh(db_document)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise Exception(f'File create failed: {str(e)}')


def create_question_answer_of_document(db: Session, document_name: str, question: str, answer: str):
    try:
        query = select(models.Document).where(models.Document.name == document_name)
        document = db.execute(query).scalar()

        if not document:
            raise Exception(f"Document with name '{document_name}' not found.")

        db_question_answer = models.QuestionAnswer(document_id=document.id, question=question, answer=answer)

        db.add(db_question_answer)
        db.commit()
        db.refresh(db_question_answer)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise Exception(f'Question Answer create failed: {str(e)}')
