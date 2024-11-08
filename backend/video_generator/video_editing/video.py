import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def add_audio_to_video(audio_file, output_video, output_folder="temp_clips"):
    # Define the path to the clips folder located in assets/background_clips
    background_clips_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, "assets", "background_clips")
    )

    # Ensure the background clips folder exists
    if not os.path.exists(background_clips_folder):
        raise FileNotFoundError(f"The folder {background_clips_folder} does not exist.")

    # Load all video files from the specified folder
    background_clips = [
        os.path.join(background_clips_folder, f)
        for f in os.listdir(background_clips_folder)
        if f.lower().endswith(".mp4")
    ]

    if not background_clips:
        raise FileNotFoundError(f"No .mp4 files found in the folder: {background_clips_folder}")

    # Shuffle the background clips for random order
    random.shuffle(background_clips)

    # Load the generated audio file to get its duration
    audio = AudioFileClip(audio_file).volumex(0.85)
    audio_duration = audio.duration

    clips = []
    total_duration = 0

    try:
        # Loop through background clips and trim them to fit audio duration
        for clip_file in background_clips:
            clip = VideoFileClip(clip_file)
            clip_duration = clip.duration

            if total_duration + clip_duration > audio_duration:
                # Trim the clip to match the remaining duration
                remaining_duration = audio_duration - total_duration
                clip = clip.subclip(0, remaining_duration)
                clips.append(clip)
                total_duration += remaining_duration
                break
            else:
                clips.append(clip)
                total_duration += clip_duration

        # Concatenate the video clips
        final_clip = concatenate_videoclips(clips)

        # Set the generated audio as the video’s audio
        final_clip = final_clip.set_audio(audio)

        # Ensure the output folder exists
        output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, output_folder))
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_path = os.path.join(output_folder, output_video)

        # Write the final video file
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        print(f"Final video saved at: {output_path}")
        return output_path

    finally:
        # Close all clips to release resources
        audio.close()
        for clip in clips:
            clip.close()

        if 'final_clip' in locals():
            final_clip.close()

