from db.database import Base
from db.models import Document

def create_table(engine):
    Base.metadata.create_all(engine)
