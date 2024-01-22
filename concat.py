import subprocess
import sys

def concatenate_videos_reencode(video1_path, video2_path, output_path):
    command = [
        'ffmpeg',
        '-i', video1_path,
        '-i', video2_path,
        '-filter_complex', '[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]',
        '-map', '[v]', '-map', '[a]',
        output_path
    ]
    subprocess.run(command, check=True)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <video1_path> <video2_path> <output_path>")
        sys.exit(1)
    concatenate_videos_reencode(sys.argv[1], sys.argv[2], sys.argv[3])
