from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://amanda@localhost/ao3_bookmarks"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    """Initialize the database and create tables."""
    from database.models import Bookmark  # Import models
    Base.metadata.create_all(bind=engine)
