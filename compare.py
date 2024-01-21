import subprocess
import json

def get_video_info(video_path):
    ffprobe_cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,r_frame_rate,duration',
        '-of', 'json',
        video_path
    ]

    result = subprocess.run(ffprobe_cmd, capture_output=True, text=True)

    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            stream = data['streams'][0]
            width, height = stream['width'], stream['height']
            frame_rate = eval(stream['r_frame_rate'])  # Evaluates the string to calculate the frame rate
            duration = float(stream['duration'])  # Converts string to float
            return {
                'Width': width,
                'Height': height,
                'Frame Rate': frame_rate,
                'Duration': duration
            }
        except (json.JSONDecodeError, KeyError, IndexError):
            print(f"Error parsing ffprobe output for {video_path}.")
            return None
    else:
        print(f"Error running ffprobe for {video_path}:")
        print(result.stderr)
        return None

def compare_videos(video1_path, video2_path):
    video1_info = get_video_info(video1_path)
    video2_info = get_video_info(video2_path)

    if video1_info is None or video2_info is None:
        return

    headers = ['Property', 'Video 1', 'Video 2']
    print(f"{headers[0]:<15} | {headers[1]:<20} | {headers[2]:<20}")
    print('-' * 60)

    for key in video1_info:
        print(f"{key:<15} | {video1_info[key]:<20} | {video2_info[key]:<20}")

if __name__ == "__main__":
    input_video_path = "input.mp4"
    output_video_path = "reversed_input.mp4"

    compare_videos(input_video_path, output_video_path)
