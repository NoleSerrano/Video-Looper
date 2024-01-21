import subprocess
import sys
import os

def get_video_info(filename):
    """Get the duration and frame rate of the video."""
    # Get the duration
    duration_result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
         '-of', 'default=noprint_wrappers=1:nokey=1', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    duration = float(duration_result.stdout.strip())

    # Get the frame rate
    framerate_result = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0', 
         '-show_entries', 'stream=avg_frame_rate', 
         '-of', 'default=noprint_wrappers=1:nokey=1', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    num, den = map(int, framerate_result.stdout.strip().split('/'))
    framerate = num / den if den != 0 else 0

    return duration, framerate

def format_timestamp(seconds, frame_rate):
    """Format timestamp as HH:MM:SS:frame_count."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_int = int(seconds % 60)
    frame_count = int((seconds - int(seconds)) * frame_rate)
    return f"{hours:02d}:{minutes:02d}:{seconds_int:02d}:{frame_count}"

def reverse_and_append_video(video_path, loops):
    # Temporary files
    reversed_video = 'temp_reversed.mp4'
    concat_list_file = 'concat_list.txt'
    final_video = 'final_output.mp4'

    # Reverse the video
    subprocess.run([
        'ffmpeg', '-i', video_path, 
        '-vf', 'reverse', 
        '-af', 'areverse', 
        reversed_video
    ], check=True)

    # Get duration and frame rate of the original video
    original_duration, frame_rate = get_video_info(video_path)

    # Create a list file for concatenation
    with open(concat_list_file, 'w') as f:
        for _ in range(loops):
            f.write(f"file '{video_path}'\n")
            f.write(f"file '{reversed_video}'\n")

    # Concatenate using the concat demuxer
    subprocess.run([
        'ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_list_file,
        '-c', 'copy', final_video
    ], check=True)

    # Calculate and print concatenation points
    for i in range(loops * 2):
        concat_point = original_duration * (i + 1)
        timestamp = format_timestamp(concat_point, frame_rate)
        print(f"Concatenation point {i+1}: {timestamp}")

    # Clean up
    os.remove(reversed_video)
    os.remove(concat_list_file)

    print(f"Final video saved as {final_video}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        reverse_and_append_video(sys.argv[1], int(sys.argv[2]))
    else:
        print("Usage: python script.py <video_path> <loops>")
