import subprocess
import sys
import os

def get_video_info(filename):
    """Get the frame rate and frame count of the video."""
    # Get frame count
    framecount_result = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
         '-show_entries', 'stream=nb_frames',
         '-of', 'default=noprint_wrappers=1:nokey=1', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    frame_count = int(framecount_result.stdout.strip())

    # Get frame rate
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

    return frame_count, framerate

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

    # Get frame count and frame rate of the original video
    original_frame_count, frame_rate = get_video_info(video_path)

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

    # Calculate and print concatenation points in frame count
    total_frames = 0
    for i in range(loops * 2):
        total_frames += original_frame_count
        print(f"Concatenation point {i+1}: {total_frames} frames")

    # Clean up
    os.remove(reversed_video)
    os.remove(concat_list_file)

    # Print frame counts
    final_frame_count, _ = get_video_info(final_video)
    print(f"Original video length: {original_frame_count} frames")
    print(f"Reversed video length: {original_frame_count} frames")  # Same as original
    print(f"Final video length: {final_frame_count} frames")
    print(f"Final video saved as {final_video}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        reverse_and_append_video(sys.argv[1], int(sys.argv[2]))
    else:
        print("Usage: python script.py <video_path> <loops>")
