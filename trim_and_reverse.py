import subprocess
import sys
import os

def get_stream_duration(video_path, stream_specifier):
    """Get the duration of the specified stream (video or audio)."""
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', stream_specifier,
        '-show_entries', 'stream=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def trim_video(video_path, duration):
    """Trim the video and audio streams to the specified duration."""
    trimmed_output = os.path.splitext(video_path)[0] + '_trimmed.mp4'
    cmd = [
        'ffmpeg', '-i', video_path,
        '-t', str(duration),
        '-async', '1',  # Synchronize audio to video duration
        trimmed_output
    ]
    subprocess.run(cmd, check=True)
    return trimmed_output

def reverse_video_and_audio(video_path, video_duration, audio_duration):
    """Reverse the video and audio streams with the audio trimmed by the delta to match the video."""
    # Calculate the delta
    delta = audio_duration - video_duration
    
    # Print the delta
    print(f"Delta (audio - video) duration: {delta} seconds")

    # Prepare the output file name
    reversed_output = os.path.splitext(video_path)[0] + '_trimmed_reversed.mp4'

    # Determine if we need to trim the audio to match the video duration
    audio_filters = 'asetpts=PTS-STARTPTS,areverse'
    if delta > 0:
        # Trim the start of the audio by the delta amount before reversing
        audio_filters = f'asetpts=PTS-STARTPTS,atrim=start={delta},areverse'

    # Command to reverse both video and audio streams, resetting timestamps and trimming the audio if needed
    cmd = [
        'ffmpeg', '-i', video_path,
        '-filter_complex',
        f'[0:v]setpts=PTS-STARTPTS,reverse[v];[0:a]{audio_filters}[a]',
        '-map', '[v]', '-map', '[a]',
        '-to', str(video_duration),  # Ensure that the output duration matches the video duration
        reversed_output
    ]

    # Run the command
    subprocess.run(cmd, check=True)
    return reversed_output


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python trim_and_reverse.py <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]
    video_duration = get_stream_duration(video_path, 'v:0')
    audio_duration = get_stream_duration(video_path, 'a:0')

    # Trim the video first to match the video duration
    trimmed_output = trim_video(video_path, video_duration)
    print(f"Trimmed video saved as {trimmed_output}")

    # Reverse the video and audio, considering any delta in durations
    trimmed_reversed_output = reverse_video_and_audio(trimmed_output, video_duration, audio_duration)
    print(f"Trimmed and reversed video saved as {trimmed_reversed_output}")
