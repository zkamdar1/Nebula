import openai
import time
import os
from dotenv import load_dotenv
from moviepy.editor import AudioFileClip, concatenate_audioclips


# Load environment variables from .env file
load_dotenv()

# Access the keys
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None or openai_api_key.strip() == "":
    raise ValueError("OpenAI API key not found. Please ensure it is set in the .env file.")

# Set the OpenAI API key
openai.api_key = openai_api_key

def generate_audio(script_text, output_folder="temp_clips"):

    # Define the path to the output folder, one level up from the current script, then into "temp_clips"
    output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, output_folder))

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    timestamp = int(time.time())

    # Generate the output audio file name using the first word, saved in the specified folder
    output_audio_file = os.path.join(output_folder, f"output_audio_{timestamp}.mp3")

    # Call the API to create the audio content
    response = openai.audio.speech.create(
        model="tts-1",
        input=script_text,
        voice="echo",
    )

    # Write the audio file to the specified folder
    with open(output_audio_file, 'wb') as audio_file:
        audio_file.write(response.content)

    # Define the path to the silence.mp3 in the assets/background_clips folder
    background_clips_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "assets", "background_clips", "silence.mp3"))

    # Add silence to the end of the audio
    original_audio = AudioFileClip(output_audio_file)
    silence_duration = 1.5  # 1.5 seconds of silence
    
    silent_audio = AudioFileClip(background_clips_path).set_duration(silence_duration)

    # Concatenate original audio with silent audio
    final_audio = concatenate_audioclips([original_audio, silent_audio])

    # Write the final audio to a new file
    final_output_audio_file = os.path.join(output_folder, f"output_audio_final_{timestamp}.mp3")
    final_audio.write_audiofile(final_output_audio_file)

    return final_output_audio_file


# Example usage
#if __name__ == "__main__":
#    script = "AI can help solve complex healthcare problems by analyzing medical data."
#    generate_audio(script)
