import subprocess
import json
import os
import sys

def get_video_info(video_path):
    ffprobe_cmd = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'stream=index,codec_name,width,height,r_frame_rate,duration,bit_rate,pix_fmt,codec_type,sample_rate,channels,nb_frames',
        '-show_entries', 'format=bit_rate,duration',
        '-show_entries', 'stream_tags=color_range,color_space,color_transfer,color_primaries',
        '-of', 'json',
        video_path
    ]

    result = subprocess.run(ffprobe_cmd, capture_output=True, text=True)

    # Print the raw JSON output for diagnostic purposes
    # print("\nffprobe output for " + video_path + ":")
    # print(result.stdout)

    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            video_stream = next((s for s in data['streams'] if s.get('codec_type') == 'video'), None)
            audio_stream = next((s for s in data['streams'] if s.get('codec_type') == 'audio'), None)

            # Print the video and audio stream data
            # print("\nVideo Stream Data for " + video_path + ":")
            # print(json.dumps(video_stream, indent=4))
            # print("\nAudio Stream Data for " + video_path + ":")
            # print(json.dumps(audio_stream, indent=4))

            info = {
                'Width': video_stream.get('width', 'N/A'),
                'Height': video_stream.get('height', 'N/A'),
                'Frame Rate': eval(video_stream['r_frame_rate']) if 'r_frame_rate' in video_stream else 'N/A',
                'Video Duration': video_stream.get('duration', 'N/A'),
                'Video Bitrate': f"{int(video_stream.get('bit_rate', '0')) // 1000} kbps",
                'Video Codec': video_stream.get('codec_name', 'N/A'),
                'Pixel Format': video_stream.get('pix_fmt', 'N/A'),
                'Audio Codec': audio_stream.get('codec_name', 'N/A'),
                'Audio Bitrate': f"{int(audio_stream.get('bit_rate', '0')) // 1000} kbps",
                'Audio Sample Rate': audio_stream.get('sample_rate', 'N/A'),
                'Audio Channels': audio_stream.get('channels', 'N/A'),
                'Audio Duration': audio_stream.get('duration', 'N/A'),
                'Overall Duration': data['format'].get('duration', 'N/A'),
                'Overall Bitrate': f"{int(data['format'].get('bit_rate', '0')) // 1000} kbps",
                'Frame Count': int(video_stream.get('nb_frames', 0)) if 'nb_frames' in video_stream else 'N/A'
            }

            return info
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"Error parsing ffprobe output for {video_path}: {e}")
            return None
    else:
        print(f"Error running ffprobe for {video_path}:")
        print(result.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        print("Usage: python script.py <video_path>")
        sys.exit(1)

    video_info = get_video_info(video_path)

    # Header with separator line
    headers = ["Video File", video_path]
    print(f"{headers[0]:<20}| {headers[1]}")
    print('-' * 85)

    if video_info:
        for key, value in video_info.items():
            print(f"{key:20}| {value}")
