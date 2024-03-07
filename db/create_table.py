from db.database import Base
from db.model import Document

def create_table(engine):
    Base.metadata.create_all(engine)
