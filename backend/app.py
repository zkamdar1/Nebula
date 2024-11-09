from fastapi import FastAPI, Depends
from api import generate  # Import the router for video generation (generate.py)
from api import health
from api import auth  # Import the router for authentication (auth.py)
from api import projects  # Import the router for project management (projects.py)
from sqlalchemy.orm import Session
from utils.database import SessionLocal
from utils.database import init_db
from api import generate  # Import the router for video generation (generate.py)
from api import auth  # Import the router for authentication (auth.py)
from api import projects  # Import the router for project management (projects.py)
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
app.include_router(generate.router, prefix="/api/generate", tags=["Video Generation"])
app.include_router(health.router, prefix="/api/health", tags=["Health Check"])
#app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
#app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
