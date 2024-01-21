import subprocess
import time
import pytz
import json
from datetime import datetime, timedelta


def get_seconds_until_next_hour():
    now = datetime.now()
    next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    return (next_hour - now).seconds

def record_stream(rtsp_url, duration=3600):
    # Define the output file name with timestamp
    now_utc = datetime.now(pytz.utc)
    # Convert UTC time to Shanghai/Asia time
    now_shanghai = now_utc.astimezone(pytz.timezone('Asia/Shanghai'))

    # Output file name with timestamp in Shanghai/Asia time
    output_file = "hyL1-"+now_shanghai.strftime("%Y-%m-%d_%H-%M") + ".mkv"

    print(duration, output_file)
    time.sleep(0.1)

    # FFmpeg command to capture the stream without re-encoding
    ffmpeg_command = [
        'ffmpeg',
        '-rtsp_transport', 'tcp',
        '-i', rtsp_url,
        '-t', str(duration),
        '-c:v', 'copy',  # Copy the video stream as is
        #'-c:a', 'copy',  # Copy the audio stream as is (if present)
        '-c:a', 'libopus', '-b:a', '24k', # Copy the audio stream as is (if present)
        '-metadata', 'title=',  # Set the metadata title
        output_file
    ]

    # Execute the FFmpeg command
    subprocess.run(ffmpeg_command)

# Run the recording function every 1hour
rtsp_url = ""
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    rtsp_url = config['rtsp_urls'][0]
while True:
    record_stream(rtsp_url, get_seconds_until_next_hour())
    
