import subprocess
import os
import shutil

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

def main(input_video, num_loops):

    # Step 1: Trim the original input
    print("Trimming the original input...")
    trim_video(input_video, 'temp1.mp4') # trimmed input

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

    return

if __name__ == "__main__":
    input_video = 'input.mp4'  # Replace with your video file name or use sys.argv to pass it as an argument
    num_loops = 3
    main(input_video, num_loops)
