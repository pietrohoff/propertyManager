from sqlmodel import SQLModel, create_engine, Session
from ..core.config import settings

DATABASE_URL = f"sqlite:///{settings.db_path}"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    from ..models.property import Property  # ensure model imported
    SQLModel.metadata.create_all(engine)
