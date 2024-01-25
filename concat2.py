import subprocess
import sys
import os

def concatenate_videos(video_files, output_file):
    temp_file = 'concat_list.txt'

    try:
        # Create a temporary file listing all videos to be concatenated
        with open(temp_file, 'w') as file:
            for video in video_files:
                file.write(f"file '{video}'\n")

        # Construct the FFmpeg command
        command = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', temp_file,
            '-c', 'copy',  # Copy the streams without re-encoding
            output_file
        ]

        subprocess.run(command, check=True)
        print("Video concatenation complete.")

    except subprocess.CalledProcessError as e:
        print(f"Error during concatenation: {e}")

    finally:
        # Remove the temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python concatenate_videos.py <video1> <video2> [<video3> ...] <output_file>")
        sys.exit(1)

    # The last argument is the output file
    output_file = sys.argv[-1]
    # All other arguments are input files
    video_files = sys.argv[1:-1]

    concatenate_videos(video_files, output_file)
