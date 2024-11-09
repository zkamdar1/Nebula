# SQLAlchemy setup and database models
import json
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

def get_secret():

    #secret_name = os.getenv("SECRET_NAME")
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId="rds!db-64a38d98-68a9-4c36-a088-3ae9bfa5ba2d"
        )
    except ClientError as e:
        print("Secret get failed")

    secret = json.loads(get_secret_value_response['SecretString'])
    passw = secret['password']

    return passw

    # Your code goes here.



def test_db_connection():
    ENDPOINT = os.getenv("AWS_ENDPOINT")
    PORT = int(os.getenv("AWS_PORT", 5432))
    USER = os.getenv("AWS_USER")
    DBNAME = os.getenv("AWS_DBNAME")
    
    # Connect to the database
    try:
        secret = get_secret()
        conn = psycopg2.connect(
            host=ENDPOINT,
            port=PORT,
            database=DBNAME,
            user=USER,
            password=secret,
            sslmode='require'
        )
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        print(f"Connection successful! Current time from DB: {result[0]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Failed to generate auth token: {e}")
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    test_db_connection()
