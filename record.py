import subprocess
import time
import pytz
import json
from datetime import datetime, timedelta

base_dir = "/var/www/nvr/"

def get_seconds_until_next_hour():
    now = datetime.now()
    next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    return (next_hour - now).seconds + 5

def get_ip_from_rtsp_url(rtsp_url):
    # Find the position of '@' and ':' after 'rtsp://'
    at_pos = rtsp_url.find('@')
    if at_pos == -1:
        return None  # Invalid RTSP URL

    colon_pos = rtsp_url.find(':', at_pos)
    if colon_pos == -1:
        return None  # Invalid RTSP URL

    # Extract the IP address part
    ip_address = rtsp_url[at_pos + 1:colon_pos]

    # Replace dots with hyphens
    modified_ip_address = ip_address.replace('.', '-')
    return modified_ip_address

def record_stream(rtsp_url, duration=3600):
    # Define the output file name with timestamp
    now_utc = datetime.now(pytz.utc)
    # Convert UTC time to Shanghai/Asia time
    now_shanghai = now_utc.astimezone(pytz.timezone('Asia/Shanghai'))

    sub_dir = now_utc.astimezone(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d") + "/"
    #mkdir focefully
    subprocess.run(["mkdir", "-p", base_dir+sub_dir])

    # Output file name with timestamp in Shanghai/Asia time
    output_file = base_dir + sub_dir +get_ip_from_rtsp_url(rtsp_url)+"_"+now_shanghai.strftime("%Y-%m-%d_%H-%M") + ".mkv"

    print(duration, output_file)
    time.sleep(0.1)

    # FFmpeg command to capture the stream without re-encoding
    ffmpeg_command = [
        'ffmpeg', '-y',
        '-rtsp_transport', 'tcp',
        '-i', rtsp_url,
        '-t', str(duration),
        '-c:v', 'copy',  # Copy the video stream as is
        '-c:a', 'copy',  # Copy the audio stream as is (if present)
        #'-c:a', 'libopus', '-b:a', '16k', # Copy the audio stream as is (if present)
        '-metadata', 'title=',  # Set the metadata title
        output_file
    ]
    print(ffmpeg_command)
    # Execute the FFmpeg command
    subprocess.run(ffmpeg_command)

# Run the recording function every 1hour
rtsp_url = ""
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    rtsp_url = config['rtsp_urls'][0]
while True:
    record_stream(rtsp_url, get_seconds_until_next_hour())
    
