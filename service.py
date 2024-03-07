from fastapi import HTTPException, status
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

        error_message = str(e)
        print(error_message)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'File create failed: {error_message}'
        )
