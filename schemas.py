from pydantic import BaseModel


class AskQuestion(BaseModel):
    document_name: str
    question: str


class Answer(BaseModel):
    document_name: str
    question: str
    answer: str
