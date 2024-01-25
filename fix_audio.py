import subprocess
import sys

def process_video(input_file, output_file):
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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_video.py <input_mp4> <output_file>")
        sys.exit(1)

    process_video(sys.argv[1], sys.argv[2])

