# Nebula - Automatic Video Generator Project

Welcome to **Nebula**, an automatic video generator project. Nebula takes a topic and turns it into a complete video with background visuals, corresponding audio narration, and subtitles. This README provides a comprehensive overview of the project, the tools and technologies used, setup instructions, and how the backend operates.

## Table of Contents

- [Project Overview](#project-overview)
- [Tools and Technologies](#tools-and-technologies)
- [Folder and File Structure](#folder-and-file-structure)
- [Backend Architecture](#backend-architecture)
  - [FastAPI](#fastapi)
  - [SQLAlchemy](#sqlalchemy)
  - [PostgreSQL & AWS RDS](#postgresql--aws-rds)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup Steps](#setup-steps)
- [Running the Application](#running-the-application)
  - [Using Docker](#using-docker)
  - [Accessing FastAPI Documentation](#accessing-fastapi-documentation)
- [API Endpoints](#api-endpoints)
- [Step-by-Step Process](#step-by-step-process)
- [Future Improvements](#future-improvements)
- [Contact](#contact)

---

## Project Overview

**Nebula** is a Python-based project that automates the creation of videos from a given topic. Leveraging various tools and services, Nebula seamlessly integrates script generation, audio narration, video editing, subtitle creation, and music integration to produce high-quality videos.

### Key Features

1. **Script Generation**: Uses OpenAI's GPT model to generate a script based on a user-provided topic.
2. **Audio Narration**: Converts the generated script into audio using Google Text-to-Speech.
3. **Video Editing**: Combines background video clips with the generated audio to create a cohesive video.
4. **Subtitle Generation**: Utilizes Google's Speech-to-Text API to generate subtitles and integrates them into the video.
5. **Music Integration**: Adds background music to enhance the video's quality.
6. **Final Output**: Produces a complete video with visuals, narration, music, and subtitles.

### Build and run the Docker containers and FASTAPI
docker-compose up --build

http://0.0.0.0:8000/docs#/
---

## Tools and Technologies

Nebula employs a combination of powerful tools and technologies to achieve its functionality:

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **SQLAlchemy**: A powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **PostgreSQL**: An advanced open-source relational database system.
- **AWS RDS (Relational Database Service)**: A managed service that makes it easy to set up, operate, and scale a relational database in the cloud.
- **Docker**: A platform for developing, shipping, and running applications in containers.
- **pgAdmin**: A popular open-source administration and development platform for PostgreSQL.
- **Python-dotenv**: A tool for managing environment variables.
- **Uvicorn**: A lightning-fast ASGI server implementation, using uvloop and httptools.

---

## Folder and File Structure

Here's a detailed explanation of the Nebula project folder and file structure:



```
/nebula
│
├── /backend                  # Backend Directory (API, Logic, Database)
│   ├── Dockerfile            # Dockerfile for containerizing backend (Python + FastAPI)
│   ├── app.py                # Main FastAPI application entry point
│   ├── /api                  # API Endpoints
│   │   ├── __init__.py
│   │   ├── auth.py           # Endpoints for authentication (register, login)
│   │   ├── projects.py       # Endpoints for managing projects (create, update, get)
│   │   └── generate.py       # Endpoint to initiate video generation
│   ├── /video_generator      # Video generation functionality
│   │   ├── __init__.py
│   │   ├── /full_generation # Main video generation logic
│   │   ├── /audio_gen
│   │   ├── /script_gen
│   │   ├── /music_generation      # Additional effects functions (tone, style)
│   │   └──/ temp_videos       # Temporary storage for videos before uploading
│   │   └── /assets         # Manage music and background assets
│   ├── /models                # Database models
│   ├── /schemas                # Pydantic models for request/response validation
│   ├── /utils                # Utility scripts and helper functions
│   │   ├── __init__.py
│   │   ├── database.py       # SQLAlchemy setup and AWS RDS setup
│   │   ├── s3_client.py      # Functions to upload/download from AWS S3
│   │   ├── firebase_utils.py # Helper functions for Firebase authentication (new)
│   │   └── utils.py     # Helper functions for JWT and additional authentication  
│
├── /frontend                 # Frontend Directory (React-based)
│   ├── /public               # Public assets for React app
│   ├── /src                  # Source code for React app
│   │   ├── /components       # Reusable components
│   │   │   ├── ProjectCard.js # Project cards for dashboard
│   │   │   ├── Navbar.js      # Navbar component
│   │   │   ├── LoginForm.js   # Login form for authentication (Firebase integration)
│   │   ├── /pages            # Main pages of the application
│   │   │   ├── Dashboard.js   # User dashboard displaying project cards
│   │   │   ├── ProjectPage.js # Page to view and edit individual projects
│   │   │   └── LoginPage.js   # User login page
│   │   ├── /services         # Axios API services
│   │   │   ├── api.js         # API service functions for communicating with the backend
│   │   ├── /firebase         # Firebase setup and utilities (new)
│   │   │   ├── firebase.js    # Firebase initialization and config (automatically generated)
│   │   │   ├── auth.js        # Functions for Firebase authentication (login, register)
│   │   ├── App.js            # Main React component
│   │   ├── index.js          # ReactDOM entry point
│   │   └── App.css           # Styling for the React components
│   └── package.json          # React dependencies
│
├── /deployment               # Deployment and Infrastructure Configuration
│   ├── nginx.conf            # Nginx configuration for load balancing
│   ├── Dockerfile.frontend   # Dockerfile for containerizing frontend
│   ├── kubernetes.yaml       # Kubernetes configuration for scalability (optional)
│   └── cloudformation.yaml   # AWS CloudFormation for managing cloud resources (optional)
│   ── docker-compose.yml    # Docker Compose configuration for backend services
│   ── requirements.txt      # Python dependencies
│   ── .env
│   ── .gitignore
└── README.md                 # Project documentation
```

## Step-by-Step Process
This section explains the process of generating a video using Nebula, along with the associated files.

### 1. Script Generation
**File**: `script_generation/script.py`

- The first step is to generate a script based on a user-provided topic. Nebula uses OpenAI's GPT model to create a script that serves as the narration for the video.
- The script text is generated when you run the `app.py` script, which calls the `generate_script()` function from `script_generation/script.py`.

### 2. Audio Generation
**File**: `audio_generation/audio.py`

- Once the script is generated, Nebula converts it into an audio file using Google Text-to-Speech.
- The `generate_audio()` function in `audio_generation/audio.py` takes the script text and generates an audio file, which is saved in the `audio_outputs/` folder.

### 3. Video Editing
**Files**: `video_editing/video.py`, `background_clips/`

- In this step, Nebula takes the background clips stored in the `background_clips/` folder and combines them with the generated audio.
- The `add_audio_to_video()` function from `video_editing/video.py` handles video concatenation, trims clips to match the length of the audio, and adds the audio to the video.
- The output video with audio is stored in the `audio_vids/` folder.

### 4. Subtitle Generation
**Files**: `sub_generation/sub.py`, `transcripts/`

- Nebula uses Google's Speech API to transcribe the audio and generate word-level subtitle timings. The subtitles are saved as SRT files in the `transcripts/` folder.
- The `generate_word_level_srt()` function in `sub_generation/sub.py` creates the SRT file, while `add_subtitles_to_video()` adds the subtitles to the final video.
- The output video with subtitles is saved in the `sub_vids/` folder.

### 5. Music Integration
**Files**: `music_generation/music.py`, `music_clips/`

- Nebula adds background music to enhance the overall video experience. Music clips are stored in the `music_clips/` folder.
- The `add_music_to_video()` function in `music_generation/music.py` handles adding background music to the video.

### 6. Final Output
**Folder**: `final_videos/`

- The final video, complete with background visuals, audio narration, music, and subtitles, is saved in the `final_videos/` folder.

## How to Use Nebula
### Prerequisites
- Python 3.7 or higher
- API keys for OpenAI and Google Cloud Speech-to-Text
- Dependencies listed in `requirements.txt`

### Installation
1. Clone the repository to your local machine:
   ```sh
   git clone https://github.com/yourusername/nebula.git
   ```
2. Navigate to the project directory:
   ```sh
   cd nebula
   ```
3. Create a virtual environment and activate it:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```
4. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Running Nebula
1. Set your OpenAI and Google Cloud API keys:
   ```sh
   export OPENAI_API_KEY="your_openai_api_key"
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/google_credentials.json"
   ```
2. Run the main application:
   ```sh
   python -m backend.app
   ```
3. Follow the prompts to generate a video. The final video will be saved in the `final_videos/` folder.

## Future Improvements
- **Web Interface**: Implement a web-based interface for ease of use.
- **User Management**: Add user authentication and allow users to save and view their generated videos.
- **Advanced Editing**: Incorporate more sophisticated video effects and transitions.


## Contact
For any questions or suggestions, please contact [Your Name](mailto:your.email@example.com).

---
Thanks for checking out Nebula! We hope you enjoy using this automatic video generator.

