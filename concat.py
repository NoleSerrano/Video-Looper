import subprocess
import os

def concatenate_videos(video1_path, video2_path, output_path):
    # Create a temporary file to list the videos for concatenation
    with open('concat_list.txt', 'w') as file:
        file.write(f"file '{video1_path}'\n")
        file.write(f"file '{video2_path}'\n")

    # Run the FFmpeg command for concatenation
    subprocess.run([
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', 'concat_list.txt',
        '-c', 'copy',
        output_path
    ], check=True)

    # Clean up the temporary file
    os.remove('concat_list.txt')

# Replace 'video1.mp4' and 'video2.mp4' with the paths to your video files
concatenate_videos('input.mp4', 'reversed_input.mp4', 'output.mp4')
