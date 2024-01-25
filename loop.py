import subprocess
import sys
import os
import shutil

def swap_files(file1, file2):
    temp_file = file1 + "_temp"
    os.rename(file1, temp_file)
    os.rename(file2, file1)
    os.rename(temp_file, file2)

def clone_file(source_path, destination_path):
    shutil.copy2(source_path, destination_path)

def concatenate_videos(video_files, output_file, count):
    temp_file = 'concat_list.txt'

    try:
        # Create a temporary file listing all videos to be concatenated, repeated by count
        with open(temp_file, 'w') as file:
            for _ in range(count):
                for video in video_files:
                    file.write(f"file '{video}'\n")

        # Construct the FFmpeg command
        command = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', temp_file,
            '-c', 'copy',  # Copy the streams without re-encoding
            output_file
        ]

        subprocess.run(command, check=True)
        print("Video concatenation complete.")

    except subprocess.CalledProcessError as e:
        print(f"Error during concatenation: {e}")

    finally:
        # Remove the temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

def reverse_video(input_file, output_file):
    try:
        command = [
            'ffmpeg', '-y',
            '-i', input_file,
            '-filter_complex', '[0:v]reverse[v];[0:a]areverse[arev]',
            '-map', '[v]',
            '-map', '[arev]',
            '-c:v', 'libx264',  # Re-encode the video
            '-c:a', 'pcm_s16le',  # Keep PCM audio codec
            output_file
        ]

        subprocess.run(command, check=True)
        print("Video reversal complete.")

    except subprocess.CalledProcessError as e:
        print(f"Error during reversal: {e}")

def fix_audio(input_file, output_file):
    try:
        # Extract the duration of the video
        video_duration = float(subprocess.check_output(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=duration', 
             '-of', 'default=noprint_wrappers=1:nokey=1', input_file], text=True).strip())

        # Construct the FFmpeg command
        command = [
            'ffmpeg', '-y',
            '-i', input_file,
            '-filter_complex',
            f"[0:a]atrim=end={video_duration},asetpts=PTS-STARTPTS[aud];[0:v]copy[v]",
            '-map', '[v]',
            '-map', '[aud]',
            '-c:v', 'libx264',  # Re-encode the video
            '-c:a', 'pcm_s16le',  # PCM audio codec
            output_file
        ]

        subprocess.run(command, check=True)
        print("Video processing complete.")

    except subprocess.CalledProcessError as e:
        print(f"Error during processing: {e}")


def main(input_video, num_loops):
    # Step 1: Fix the audio
    print("Trimming the original input...")
    fix_audio(input_video, 'temp1.mp4') # trimmed input

    # Step 2: Reverse the video
    print("Reversing the trimmed input...")
    reverse_video('temp1.mp4', 'temp2.mp4') # reversed

    # Step 3: Concatenate and reversed videos
    print("Concatenating trimmed and reversed videos...")
    output_path = os.path.splitext(input_video)[0] + f'_looped_{num_loops}.mp4'
    concatenate_videos(['temp1.mp4', 'temp2.mp4'], output_path, num_loops) # looped video

    os.remove('temp1.mp4')
    os.remove('temp2.mp4')

    return

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <video> <num_loops>")
        sys.exit(1)
    input_video = sys.argv[1]  # Replace with your video file name or use sys.argv to pass it as an argument
    num_loops = int(sys.argv[2])
    main(input_video, num_loops)
