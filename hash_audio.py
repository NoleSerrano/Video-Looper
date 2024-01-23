import subprocess
import hashlib
import glob
import os

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

def process_videos(frame_number):
    video_paths = glob.glob('*.mp4')
    hashes = []

    for video_path in video_paths:
        try:
            frame_rate, _ = get_frame_rate_and_duration(video_path)
            audio_data = extract_audio_at_frame(video_path, frame_number, frame_rate)
            audio_hash = hash_audio(audio_data)
            hashes.append(audio_hash)
        except Exception as e:
            print(f"Error processing {video_path}: {e}")
            hashes.append('Error')

    return video_paths, hashes

def print_hashes(video_paths, hashes, frame_number):
    max_name_length = max(len(os.path.basename(path)) for path in video_paths)
    column_width = max(20, max_name_length)

    headers = ['Video', f'Audio Hash at Frame {frame_number}']
    header_line = " | ".join([f"{h:<{column_width}}" for h in headers])
    print(header_line)
    print('-' * len(header_line))

    for video_path, hash_value in zip(video_paths, hashes):
        video_name = os.path.basename(video_path)
        print(f"{video_name:<{column_width}} | {hash_value}")

video_path = 'input.mp4'
frame_number = 23  # Replace with your frame number

frame_number = 23  # Replace with the frame number you want to analyze
video_paths, hashes = process_videos(frame_number)
print_hashes(video_paths, hashes, frame_number)