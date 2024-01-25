# Video Looper
This tool takes videos and creates a looped video based on specified number of loops. It handles problems of audio synchronization by first converting the mp4 file's audio stream for AAC to PCM.

## Installation
- Have python installed
- ffmpeg and ffprobe is required

## Usage
Run the loop script like such `loop.py video.mp4 1` and the output will be, in this case, video_looped_1.

## Notes 
Haven't tested with other files. And probably should add more checks to check if already using PCM.
