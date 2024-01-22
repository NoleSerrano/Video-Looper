import subprocess
import os

def trim_video(video_path):
    subprocess.run(['python', 'trim.py', video_path], check=True)

def reverse_video(video_path):
    subprocess.run(['python', 'reverse.py', video_path], check=True)

def concatenate_videos(video1_path, video2_path, output_path):
    subprocess.run(['python', 'concat.py', video1_path, video2_path, output_path], check=True)

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed: {file_path}")

def main(input_video, num_loops):
    trimmed_video = os.path.splitext(input_video)[0] + '_trimmed.mp4'
    reversed_video = os.path.splitext(trimmed_video)[0] + '_reversed.mp4'
    loop_video = os.path.splitext(input_video)[0] + '_loop.mp4'
    loop_trimmed = os.path.splitext(loop_video)[0] + '_trimmed.mp4'

    # Step 1: Trim the original input
    print("Trimming the original input...")
    trim_video(input_video)

    # Step 2: Reverse the trimmed input
    print("Reversing the trimmed input...")
    reverse_video(trimmed_video)

    # Step 3: Concatenate trimmed and reversed videos
    print("Concatenating trimmed and reversed videos...")
    concatenate_videos(trimmed_video, reversed_video, loop_video)

    # Step 4: Trim the concatenated video (loop)
    print("Trimming the concatenated loop...")
    trim_video(loop_video) # outputs loop trimmed

    concatenate_videos(loop_trimmed, loop_trimmed, 'test.mp4')
    trim_video('test.mp4')

    return

    # Step 5: Repeat concatenation and trimming for the number of loops
    current_loop_video = loop_video
    for i in range(num_loops - 1):
        next_loop_video = os.path.splitext(input_video)[0] + f'_loop{i+1}.mp4'
        print(f"Creating loop {i+1}...")
        concatenate_videos(current_loop_video, loop_video, next_loop_video)

        # Trim the newly concatenated video
        print(f"Trimming loop {i+1}...")
        trim_video(next_loop_video)

        # remove_file(current_loop_video)
        current_loop_video = os.path.splitext(next_loop_video)[0] + '_trimmed.mp4'

    # Rename the final loop video
    final = os.path.splitext(input_video)[0] + f'_looped_{num_loops}.mp4'
    os.rename(current_loop_video, final)

    # Cleanup intermediate files
    # remove_file(trimmed_video)
    # remove_file(reversed_video)
    # remove_file(loop_video)  # Only if it's not the final loop video


if __name__ == "__main__":
    input_video = 'input.mp4'  # Replace with your video file name or use sys.argv to pass it as an argument
    num_loops = 2
    main(input_video, num_loops)
