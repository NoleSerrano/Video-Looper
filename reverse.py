import subprocess
import sys
import os

def get_video_duration(video_path):
    """Get the duration of the video."""
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                             '-of', 'default=noprint_wrappers=1:nokey=1', video_path],
                            stdout=subprocess.PIPE, text=True)
    return float(result.stdout.strip())

def reverse_video(video_path):
    """Reverse the video and trim it to match the original duration."""
    duration = get_video_duration(video_path)
    output_path = os.path.splitext(video_path)[0] + '_reversed.mp4'

    subprocess.run(['ffmpeg', '-i', video_path, '-vf', 'reverse', '-af', 'areverse',
                    '-t', str(duration), output_path], check=True)
    print(f"Reversed video saved as {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python reverse.py <video_path>")
        sys.exit(1)

    reverse_video(sys.argv[1])
