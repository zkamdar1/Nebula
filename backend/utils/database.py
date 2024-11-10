# SQLAlchemy setup and database models
import json
from fastapi import logger
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
import boto3
from botocore.exceptions import ClientError
import psycopg2
'''
# Get the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an engine to connect to the PostgreSQL database
engine = create_engine(DATABASE_URL)

# Configure a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for defining models
Base = declarative_base()

def init_db():
    # Import models here to ensure they are registered with SQLAlchemy's metadata
    from utils.models import Test  # Update this import to match your actual model file and classes
    Base.metadata.create_all(bind=engine)

'''


def test_db_connection():
    ENDPOINT = os.getenv("AWS_ENDPOINT")
    PORT = (os.getenv("AWS_PORT", 5432))
    USER = os.getenv("AWS_USER")
    PASS = os.getenv("AWS_PASS")
    DBNAME = os.getenv("AWS_DBNAME")
    REGION = os.getenv("AWS_REGION")
    
    if not all([ENDPOINT, PASS, PORT, USER, DBNAME, REGION]):
        print("One or more environment variables are missing. Please check your configuration.")
        return
    
    # Connect to the database
    try:
        conn = psycopg2.connect(
            host=ENDPOINT,
            port=PORT,
            database=DBNAME,
            user=USER,
            password=PASS,
        )
        
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        print(f"Connection successful! Current time from DB: {result[0]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    test_db_connection()
