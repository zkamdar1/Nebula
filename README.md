# Nebula - Automatic Video Generator Project

Welcome to **Nebula**, an automatic video generator project. Nebula takes a topic and turns it into a complete video with background visuals, corresponding audio narration, and subtitles. Below, you'll find a detailed overview of the project structure, how it works step-by-step, and how to use it.

## Project Overview
**Nebula** is a Python-based project that generates videos automatically. It comprises several steps:

1. **Script Generation**: Generates a script based on a topic using OpenAI's GPT model.
   - Files: `script_generation/script.py`

2. **Audio Generation**: Converts the generated script into an audio narration using Google Text-to-Speech.
   - Files: `audio_generation/audio.py`

3. **Video Editing**: Combines pre-existing background video clips with the generated audio to produce a cohesive video.
   - Files: `video_editing/video.py`, `background_clips/`

4. **Subtitle Generation**: Generates subtitles from the audio using Google's Speech API and adds them to the video.
   - Files: `sub_generation/sub.py`, `transcripts/`

5. **Music Integration**: Adds background music to the video.
   - Files: `music_generation/music.py`, `music_clips/`

6. **Final Output**: The finished video with audio, music, and subtitles is saved in the `final_videos/` folder.

## Folder and File Structure
Here is a detailed explanation of the Nebula project folder and file structure:

### **Final Project Structure**

```
/video-maker-app
│
├── /backend                  # Backend Directory (API, Logic, Database)
│   ├── Dockerfile            # Dockerfile for containerizing backend (Python + FastAPI)
│   ├── docker-compose.yml    # Docker Compose configuration for backend services
│   ├── requirements.txt      # Python dependencies
│   ├── app.py                # Main FastAPI application entry point
│   ├── /api                  # API Endpoints
│   │   ├── __init__.py
│   │   ├── auth.py           # Endpoints for authentication (register, login)
│   │   ├── projects.py       # Endpoints for managing projects (create, update, get)
│   │   └── generate.py       # Endpoint to initiate video generation
│   ├── /video_generator      # Video generation functionality
│   │   ├── __init__.py
│   │   ├── generate_video.py # Main video generation logic
│   │   ├── effects.py        # Additional effects functions (tone, style)
│   │   └── assets.py         # Manage music and background assets
│   ├── /utils                # Utility scripts and helper functions
│   │   ├── __init__.py
│   │   ├── database.py       # SQLAlchemy setup and database models
│   │   ├── s3_client.py      # Functions to upload/download from AWS S3
│   │   └── auth_utils.py     # Helper functions for JWT and authentication
│   └── /data                 # Data folder for storing configurations and temporary files
│       ├── config.json       # Application configuration
│       └── temp_videos       # Temporary storage for videos before uploading
│
├── /frontend                 # Frontend Directory (React-based)
│   ├── /public               # Public assets for React app
│   ├── /src                  # Source code for React app
│   │   ├── /components       # Reusable components
│   │   │   ├── ProjectCard.js # Project cards for dashboard
│   │   │   ├── Navbar.js      # Navbar component
│   │   │   └── LoginForm.js   # Login form for authentication
│   │   ├── /pages            # Main pages of the application
│   │   │   ├── Dashboard.js   # User dashboard displaying project cards
│   │   │   ├── ProjectPage.js # Page to view and edit individual projects
│   │   │   └── LoginPage.js   # User login page
│   │   ├── /services         # Axios API services
│   │   │   ├── api.js         # API service functions for communicating with the backend
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
│
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

