# SQLAlchemy setup and database models
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import os

# Get the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("DATABASE_URL is not set in the environment variables.")

# Create the SQLAlchemy engine with connection pooling and echo for debugging
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Ensures connections are valid
    echo=True  # Set to False in production
)

# Configure a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for defining models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a SQLAlchemy session.
    Ensures that the session is closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database by creating all tables.
    Ensure all models are imported before calling this function.
    """
    from backend.models.test import Test  # Import all your models here
    Test.metadata.create_all(bind=engine)

def test_db_connection():
    """
    Test the database connection using SQLAlchemy.
    """
    try:
        # Create a new database session
        db = SessionLocal()
        # Execute a simple query to check the connection
        result = db.execute(text('SELECT NOW();')).fetchone()
        print(f"Connection successful! Current time from DB: {result[0]}")
        #init_db()
        db.close()
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise e

if __name__ == "__main__":
    test_db_connection()
