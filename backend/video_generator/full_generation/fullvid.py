from backend.video_generator.script_generation.script import generate_script
from backend.video_generator.audio_generation.audio import generate_audio
from backend.video_generator.video_editing.video import add_audio_to_video
from backend.video_generator.sub_generation.sub import add_subtitles_to_video, generate_word_level_srt, clear_folder
from backend.video_generator.music_generation.music import add_background_music
import time

def create_video_with_audio_and_subtitles():
    # Generate the script using GPT
    script_text = generate_script()
    
    timestamp = int(time.time())

    # Generate the audio from the provided script
    audio_file = generate_audio(script_text)

    # Add audio to the randomized and trimmed video clips
    video_file = add_audio_to_video(audio_file, output_video=f"final_audio{timestamp}.mp4")

    # Generate the SRT file from the audio
    srt_file = generate_word_level_srt(audio_file)

    # Add subtitles to the video
    video_with_subtitles = add_subtitles_to_video(video_file, srt_file, output_video_with_subs=f"final_sub{timestamp}.mp4")

    # Add music to final video
    final_video_with_music = add_background_music(video_with_subtitles,  output_video_file=f"finalvid{timestamp}.mp4" )

    print(f"Final Video Created: {final_video_with_music}")

    # Clean up temporary files
    clear_folder('temp_clips')

    return final_video_with_music
