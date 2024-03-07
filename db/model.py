from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from db.database import Base


class Document(Base):
    __tablename__ = 'documents'

    name = mapped_column(String(255), index=True)
