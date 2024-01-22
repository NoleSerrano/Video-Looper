import subprocess
import sys
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

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python concatenate.py <video1_path> <video2_path> <output_path>")
        sys.exit(1)

    concatenate_videos(sys.argv[1], sys.argv[2], sys.argv[3])
