import subprocess
import hashlib

def get_frame_rate_and_duration(video_path):
    cmd = [
        'ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=r_frame_rate,duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', video_path
    ]
    process = subprocess.run(cmd, capture_output=True, text=True)
    if process.returncode != 0:
        raise Exception("ffprobe error: " + process.stderr)
    frame_rate, duration = process.stdout.strip().split('\n')
    return eval(frame_rate), float(duration)

def extract_audio_at_frame(video_path, frame_number, frame_rate):
    # Calculate timestamp in seconds
    timestamp = frame_number / frame_rate
    # Extract 1 second of audio around the frame
    cmd = [
        'ffmpeg', '-ss', str(timestamp), '-t', '1', '-i', video_path,
        '-f', 'mp3', '-vn', '-'
    ]
    process = subprocess.run(cmd, capture_output=True)
    if process.returncode != 0:
        raise Exception("ffmpeg error: " + process.stderr)
    return process.stdout

def hash_audio(audio_data):
    return hashlib.sha256(audio_data).hexdigest()

video_path = 'input.mp4'
frame_number = 23  # Replace with your frame number

frame_rate, _ = get_frame_rate_and_duration(video_path)
audio_data = extract_audio_at_frame(video_path, frame_number, frame_rate)
audio_hash = hash_audio(audio_data)

print(f"Hash for audio at frame {frame_number}: {audio_hash}")
