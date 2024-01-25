import subprocess
import sys

def reverse_video(input_file, output_file):
    try:
        command = [
            'ffmpeg', '-y',
            '-i', input_file,
            '-filter_complex', '[0:v]reverse[v];[0:a]areverse[arev]',
            '-map', '[v]',
            '-map', '[arev]',
            '-c:v', 'libx264',  # Re-encode the video
            '-c:a', 'pcm_s16le',  # Keep PCM audio codec
            output_file
        ]

        subprocess.run(command, check=True)
        print("Video reversal complete.")

    except subprocess.CalledProcessError as e:
        print(f"Error during reversal: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python reverse_video.py <input_file> <output_file>")
        sys.exit(1)

    reverse_video(sys.argv[1], sys.argv[2])

