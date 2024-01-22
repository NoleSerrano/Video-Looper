import subprocess
import json
import os
import sys
import glob

# Can specify multiple videos to compare or if no args are passed, it compares all the mp4 videos in the folder

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
                'Width': video_stream.get('width', 'N/A') if video_stream else 'N/A',
                'Height': video_stream.get('height', 'N/A') if video_stream else 'N/A',
                'Frame Rate': eval(video_stream['r_frame_rate']) if video_stream else 'N/A',
                'Video Duration': video_stream.get('duration', 'N/A') if video_stream else 'N/A',
                'Video Bitrate': int(video_stream.get('bit_rate', '0')) // 1000 if video_stream else 'N/A',  # Convert to kbps
                'Video Codec': video_stream.get('codec_name', 'N/A') if video_stream else 'N/A',
                'Pixel Format': video_stream.get('pix_fmt', 'N/A') if video_stream else 'N/A',
                'Audio Codec': audio_stream.get('codec_name', 'N/A') if audio_stream else 'N/A',
                'Audio Bitrate': int(audio_stream.get('bit_rate', '0')) // 1000 if audio_stream else 'N/A',  # Convert to kbps
                'Audio Sample Rate': audio_stream.get('sample_rate', 'N/A') if audio_stream else 'N/A',
                'Audio Channels': audio_stream.get('channels', 'N/A') if audio_stream else 'N/A',
                'Audio Duration': audio_stream.get('duration', 'N/A') if audio_stream else 'N/A',
                'Overall Duration': data['format'].get('duration', 'N/A'),
                'Overall Bitrate': int(data['format'].get('bit_rate', '0')) // 1000 , # Convert to kbps
                'Frame Count': int(video_stream['nb_frames']) if 'nb_frames' in video_stream and video_stream['nb_frames'].isdigit() else 'N/A'
            }
            # Adding color information if available and if video stream exists
            if video_stream and 'tags' in video_stream:
                info.update({
                    'Color Range': video_stream['tags'].get('color_range', 'N/A'),
                    'Color Space': video_stream['tags'].get('color_space', 'N/A'),
                    'Color Transfer': video_stream['tags'].get('color_transfer', 'N/A'),
                    'Color Primaries': video_stream['tags'].get('color_primaries', 'N/A'),
                })
            return info
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"Error parsing ffprobe output for {video_path}: {e}")
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

    # Print header
    video1_name = os.path.basename(video1_path)
    video2_name = os.path.basename(video2_path)

    headers = ['Property', video1_name, video2_name]
    print(f"{headers[0]:<20} | {headers[1]:<30} | {headers[2]:<30}")
    print('-' * 85)

    # Properties for comparison
    properties = [
    'Width', 'Height', 'Frame Rate', 'Video Duration', 'Video Bitrate',
    'Video Codec', 'Pixel Format', 'Audio Codec', 'Audio Bitrate',
    'Audio Sample Rate', 'Audio Channels', 'Audio Duration',
    'Overall Duration', 'Overall Bitrate', 'Frame Count'
]

    for prop in properties:
        # Fetch properties safely, some might not be present
        val1 = video1_info.get(prop, 'N/A')
        val2 = video2_info.get(prop, 'N/A')
        print(f"{prop:<20} | {val1:<30} | {val2:<30}")

if __name__ == "__main__":
    # If no arguments are passed, compare all .mp4 files in the current directory
    if len(sys.argv) == 1:
        video_paths = glob.glob('*.mp4')
        if not video_paths:
            print("No .mp4 files found in the current directory.")
            sys.exit(1)
    else:
        video_paths = sys.argv[1:]

    video_infos = [get_video_info(path) for path in video_paths]

    if any(info is None for info in video_infos):
        print("Error getting video information.")
        sys.exit(1)

    # Print header
    headers = ['Property'] + [os.path.basename(path) for path in video_paths]
    header_line = " | ".join([f"{h:<20}" for h in headers])
    print(header_line)
    print('-' * len(header_line))

    # Properties for comparison
    properties = [
        'Width', 'Height', 'Frame Rate', 'Video Duration', 'Video Bitrate',
        'Video Codec', 'Pixel Format', 'Audio Codec', 'Audio Bitrate',
        'Audio Sample Rate', 'Audio Channels', 'Audio Duration',
        'Overall Duration', 'Overall Bitrate', 'Frame Count'
    ]

    for prop in properties:
        line = f"{prop:<20} | "
        line += " | ".join([f"{info.get(prop, 'N/A'):<20}" for info in video_infos])
        print(line)