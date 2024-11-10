from fastapi import FastAPI, Depends
from api import generate  # Import the router for video generation (generate.py)
from api import health
from api import test
from utils.database import test_db_connection
from api import generate  # Import the router for video generation (generate.py)
from contextlib import asynccontextmanager

# Use asynccontextmanager to manage startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run at startup
    test_db_connection()  # Create tables when starting the app
    yield
    # Code to run on shutdown, if needed

# Pass the lifespan context to FastAPI
app = FastAPI(lifespan=lifespan)

# Register the routers with specific prefixes for better organization
app.include_router(generate.router)
app.include_router(health.router)
app.include_router(test.router)

