import subprocess
import os

def extract_video(input_video, output_video):
    try:
        command = [
            'ffmpeg',
            '-i', input_video,
            '-c:v', 'copy',    # Copy the video stream
            '-an',             # No audio
            output_video
        ]

        subprocess.run(command, check=True)
        print(f"Video stream extracted: {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while extracting video stream: {e}")

def convert_audio_to_pcm_wav(input_video, output_audio):
    try:
        command = [
            'ffmpeg',
            '-i', input_video,
            '-acodec', 'pcm_s16le',  # PCM codec
            '-vn',                  # No video
            output_audio
        ]

        subprocess.run(command, check=True)
        print(f"Audio converted to PCM (WAV): {output_audio}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while converting audio: {e}")

def combine_video_audio(video_file, audio_file, output_file):
    try:
        command = [
            'ffmpeg',
            '-i', video_file,
            '-i', audio_file,
            '-c:v', 'copy',    # Copy the video stream
            '-c:a', 'copy',    # Copy the audio stream
            '-shortest',       # Finish encoding when the shortest stream ends
            output_file
        ]

        subprocess.run(command, check=True)
        print(f"Combined video and audio: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while combining video and audio: {e}")

# Example usage
input_video = 'input.mp4'
temp_video = 'temp_video.mp4'
temp_audio = 'temp_audio.wav'  # Change to WAV format
output_video = os.path.splitext(input_video)[0] + "_pcm.mp4"

extract_video(input_video, temp_video)
convert_audio_to_pcm_wav(input_video, temp_audio)
combine_video_audio(temp_video, temp_audio, output_video)

# Optionally, remove temporary files
os.remove(temp_video)
os.remove(temp_audio)
