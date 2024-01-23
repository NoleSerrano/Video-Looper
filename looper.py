import subprocess
import sys
import os

# DOES NOT WORK PERFECTLY

def get_video_timescale(video_path):
    """Get the timescale of the video."""
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=timescale',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        # Attempt to parse the timescale as an integer.
        timescale = int(result.stdout.strip())
    except ValueError:
        # If the output is not an integer, print an error message and exit.
        print("Unable to determine the video timescale. ffprobe output was:")
        print(result.stdout)
        # Optionally, provide a default timescale or handle the error as appropriate.
        timescale = 30000  # Example default value, adjust as needed.
        # Alternatively, you could exit the script if you don't want to assume a default value.
        # sys.exit(1)
    return timescale

def reencode_video_with_timescale(video_path, output_path, video_track_timescale):
    """Re-encode video with a specified timescale."""
    command = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-video_track_timescale', str(video_track_timescale),
        '-c', 'copy',
        output_path
    ]
    subprocess.run(command, check=True)

def reverse_video(video_path, reversed_video_path):
    """Reverse the video."""
    command = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-vf', 'reverse',
        '-af', 'areverse',
        reversed_video_path
    ]
    subprocess.run(command, check=True)

def concatenate_videos(video1_path, video2_path, output_path):
    """Concatenate two videos."""
    command = [
        'ffmpeg',
        '-y',
        '-i', video1_path,
        '-i', video2_path,
        '-filter_complex', '[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]',
        '-map', '[v]',  # Map the video from the filtergraph
        '-map', '[a]',  # Map the audio from the filtergraph
        '-c:v', 'libx264',  # Re-encode video with x264
        '-preset', 'medium',  # You can change the preset to adjust encoding speed and file size
        '-c:a', 'aac',  # Re-encode audio with aac
        '-strict', 'experimental',  # Needed if aac is experimental
        '-b:a', '192k',  # Bitrate for audio
        output_path
    ]
    subprocess.run(command, check=True)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <video_path> <output_path>")
        sys.exit(1)

    video_path = sys.argv[1]
    output_path = sys.argv[2]
    base_dir = os.path.dirname(output_path)  # Get the directory of the output file

    # Get the timescale from the original video
    timescale = get_video_timescale(video_path)

    # Define the paths for the re-encoded and reversed videos
    reencoded_video_path = os.path.join(base_dir, 'reencoded_original.mp4')
    reversed_video_path = os.path.join(base_dir, 'reversed_video.mp4')

    # Re-encode the original video with the determined timescale
    reencode_video_with_timescale(video_path, reencoded_video_path, timescale)

    # Reverse the re-encoded video
    reverse_video(reencoded_video_path, reversed_video_path)

    # Concatenate the original and reversed videos
    concatenate_videos(reencoded_video_path, reversed_video_path, output_path)

    print(f"Concatenated video saved as {output_path}")