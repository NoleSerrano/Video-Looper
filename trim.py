import subprocess
import sys
import json
import os

def get_video_duration(video_path):
    """Get the duration of the video stream."""
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def trim_audio_duration(video_path):
    """Trim the audio duration to match the video duration."""
    video_duration = get_video_duration(video_path)

    output_file = os.path.splitext(video_path)[0] + '_trimmed.mp4'
    cmd = [
        'ffmpeg', '-i', video_path,
        '-af', f'atrim=end={video_duration}',
        '-vcodec', 'copy', output_file
    ]
    subprocess.run(cmd, check=True)
    return output_file

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python trim.py <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]
    trimmed_file = trim_audio_duration(video_path)
    print(f"Trimmed video saved as {trimmed_file}")
