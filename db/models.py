from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from db.database import Base


class Document(Base):
    __tablename__ = 'documents'

    name = mapped_column(String(255), index=True, nullable=False)
    questions_answers = relationship("QuestionAnswer", back_populates="document")


class QuestionAnswer(Base):
    __tablename__ = 'questions_answers'

    question = mapped_column(Text, nullable=False)
    answer = mapped_column(Text, nullable=False)
    document_id = mapped_column(Integer, ForeignKey('documents.id'))
    document = relationship("Document", back_populates="questions_answers")
