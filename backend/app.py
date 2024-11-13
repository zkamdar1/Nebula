from fastapi import FastAPI, Depends
from api import generate  # Import the router for video generation (generate.py)
from api import health
from api import projects
from api import auth
from utils.database import init_db
from contextlib import asynccontextmanager

# Use asynccontextmanager to manage startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run at startup
    init_db()  # Create tables when starting the app
    yield
    # Code to run on shutdown, if needed

# Pass the lifespan context to FastAPI
app = FastAPI(lifespan=lifespan)

# Register the routers with specific prefixes for better organization
app.include_router(generate.router)
app.include_router(health.router)
app.include_router(projects.router)
app.include_router(auth.router)
