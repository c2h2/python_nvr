# python_nvr - RTSP Stream Recorder

This project includes a Python script for recording RTSP streams at regular intervals. Each recording session lasts for 60 minutes, and the audio codec is converted to Opus for efficient storage. This tool is useful for surveillance, monitoring, or any scenario where regular video recording from a stream is required.

## Getting Started

To use this script, you need to set up the RTSP URL in the `config.json` file. Copy the `config.json.example` to `config.json` and update the URL.

### Prerequisites

Ensure you have Python installed on your system. You will also need `ffmpeg` for handling the video stream.

### Installation
    #git clone this repo
    cp config.json.example config.json
    vim config.json #fill your stream url
    pip3 install -r requirements.txt

### Run

    python3 record.py

