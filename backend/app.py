from fastapi import FastAPI, Depends
from backend.api import generate  # Import the router for video generation (generate.py)
from backend.api import health
from backend.api import projects
from backend.api import auth
from backend.api import media
from backend.utils.database import init_db
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# Use asynccontextmanager to manage startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run at startup
    init_db()  # Create tables when starting the app
    yield
    # Code to run on shutdown, if needed

# Pass the lifespan context to FastAPI
app = FastAPI(lifespan=lifespan)

# Configure CORS
origins = [
    "http://localhost:3000",  # Replace with your frontend URL
    # Add other origins if necessary
    "http://127.0.0.1:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the routers with specific prefixes for better organization
app.include_router(generate.router)
app.include_router(health.router)
app.include_router(projects.router)
app.include_router(auth.router)
app.include_router(media.router)
