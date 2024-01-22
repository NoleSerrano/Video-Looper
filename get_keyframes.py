import subprocess

def get_keyframe_indices(video_fn):
    # Run ffprobe to get frame types
    command = ['ffprobe', '-v', 'error', '-show_entries', 'frame=pict_type', '-of', 'default=noprint_wrappers=1']
    out = subprocess.check_output(command + [video_fn]).decode()
    frame_types = out.replace('pict_type=', '').split()

    # Extract indices of I-frames (keyframes)
    i_frame_indices = [index for index, frame_type in enumerate(frame_types) if frame_type == 'I']
    return i_frame_indices

if __name__ == '__main__':
    filename = 'reversed_input.mp4'
    keyframe_indices = get_keyframe_indices(filename)
    print("Keyframe indices:", keyframe_indices)
