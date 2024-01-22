import subprocess
import os
import shutil
import math
import time

def swap_files(file1, file2):
    temp_file = file1 + "_temp"
    os.rename(file1, temp_file)
    os.rename(file2, file1)
    os.rename(temp_file, file2)

def clone_file(source_path, destination_path):
    shutil.copy2(source_path, destination_path)
    
def trim_video(video_path, output_path):
    subprocess.run(['python', 'trim.py', video_path, output_path], check=True)

def reverse_video(video_path, output_path):
    subprocess.run(['python', 'reverse.py', video_path, output_path], check=True)

def concatenate_videos(video1_path, video2_path, output_path):
    subprocess.run(['python', 'concat.py', video1_path, video2_path, output_path], check=True)

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed: {file_path}")

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

def trim_to_duration(video_path, duration_needed, output_path):
    """Trim the video to the specific duration with re-encoding."""
    cmd = [
        'ffmpeg', '-y', '-i', video_path,
        '-t', str(duration_needed),
        output_path  # Allow FFmpeg to re-encode the video
    ]
    subprocess.run(cmd, check=True)

def create_and_trim_large_loop(base_loop, num_loops):
    duration_of_one_loop = get_video_duration(base_loop)
    print(f'duration_of_one_loop = {duration_of_one_loop}')

    current_loop = base_loop
    loop_size = 1

    # Double the loop until it exceeds or meets the required number of loops
    while loop_size < num_loops:
        loop_size *= 2
        next_loop = f'temp_loop_{loop_size}.mp4'
        concatenate_videos(current_loop, current_loop, next_loop)
        trim_video(next_loop, current_loop)

    # Final trimming if the loop size is larger than needed
    excess_loops = loop_size - num_loops
    if excess_loops > 0:
        total_duration_needed = duration_of_one_loop * num_loops
        final_loop = f'final_loop_{num_loops}.mp4'
        print('total_duration_needed = {total_duration_needed}')
        trim_to_duration(current_loop, total_duration_needed, final_loop)
    else:
        final_loop = current_loop

    return final_loop

def main(input_video, num_loops):
    total_concatenation_time = 0
    total_trim_time = 0
    total_reverse_time  = 0

    # Step 1: Trim the original input
    print("Trimming the original input...")
    start_time = time.time()
    trim_video(input_video, 'temp1.mp4') # trimmed input
    end_time = time.time()
    total_trim_time += (end_time - start_time)

    # Step 2: Reverse the trimmed input
    print("Reversing the trimmed input...")
    reverse_video('temp1.mp4', 'temp2.mp4') # reversed

    # Step 3: Concatenate trimmed and reversed videos
    print("Concatenating trimmed and reversed videos...")
    concatenate_videos('temp1.mp4', 'temp2.mp4', 'temp3.mp4') # looped video

    # Step 4: Trim the concatenated video (loop)
    print("Trimming the concatenated loop...")
    trim_video('temp3.mp4', 'temp1.mp4') # outputs loop trimmed
    clone_file('temp1.mp4', 'temp2.mp4') # temp2 will be the big boy

    for i in range(num_loops - 1):
        concatenate_videos('temp1.mp4', 'temp2.mp4', 'temp3.mp4') # temp3 = bigger loop
        trim_video('temp3.mp4', 'temp4.mp4') # temp4 = bigger loop trimmed
        swap_files('temp4.mp4', 'temp2.mp4') # temp2 = bigger loop

    output_path = os.path.splitext(input_video)[0] + f'_looped_{num_loops}.mp4'
    os.remove('temp1.mp4')
    os.remove('temp3.mp4')
    os.remove('temp4.mp4')
    os.rename('temp2.mp4', output_path)

    return

if __name__ == "__main__":
    input_video = 'input.mp4'  # Replace with your video file name or use sys.argv to pass it as an argument
    num_loops = 3
    start_time = time.time()
    main(input_video, num_loops)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Script execution time: {elapsed_time} seconds")