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

def main(input_video):
    trimmed_video = os.path.splitext(input_video)[0] + '_trimmed.mp4'
    reversed_video = os.path.splitext(trimmed_video)[0] + '_reversed.mp4'
    loop_video = 'loop.mp4'
    final_trimmed_loop = 'final_trimmed_loop.mp4'

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
    trim_video(loop_video)

    # Renaming the final trimmed loop to a more descriptive name
    os.rename(loop_video, final_trimmed_loop)
    print(f"Final loop created: {final_trimmed_loop}")

    # Cleanup intermediate files
    # remove_file(trimmed_video)
    # remove_file(reversed_video)

if __name__ == "__main__":
    input_video = 'input.mp4'  # Replace with your video file name or use sys.argv to pass it as an argument
    main(input_video)
