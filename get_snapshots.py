import subprocess
import datetime
from camera_config import *

storage="/var/www/html/snapshots"



def capture_snapshot(camera):
    # Construct the RTSP URL
    rtsp_url = f"rtsp://{camera['username']}:{camera['password']}@{camera['ip']}:{camera['port']}/{camera['stream_path']}"

    # Get the current timestamp
    day = datetime.datetime.now().strftime('%Y%m%d')
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    the_dir = f"{storage}/{day}"

    # Create the directory if it doesn't exist
    try:
        subprocess.run(['mkdir', '-p', the_dir], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to create directory {the_dir}: {e}")
        sys.exit(21)
    
    # Create the output filename with timestamp
    output_file = f"{the_dir}/snapshot_{camera['ip']}_{timestamp}.jpg"

    # Command to capture a single image using ffmpeg
    ffmpeg_command = [
        'ffmpeg',
        '-i', rtsp_url,
        '-vframes', '1',
        '-q:v', '2',
        output_file
    ]

    # Run the command
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Snapshot saved as '{output_file}'")
    except subprocess.CalledProcessError as e:
        print(f"Failed to capture snapshot from {camera['ip']}: {e}")


if __name__ == '__main__':
    for camera in cameras:
        capture_snapshot(camera)