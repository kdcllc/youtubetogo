# YouTube Video Downloader and Converter

This script downloads and converts YouTube videos to either video or audio format. It can download videos from a specific channel or a single video URL.

## Requirements

1. **ffmpeg** to be installed on the system.

```bash
sudo apt install ffmpeg
```

2. If desired to download all of the videos from a specified channel then [**YouTube Data API v3**](https://console.cloud.google.com/apis/) key must be created.


## Installation

### Install from [pypi.org](https://pypi.org/project/youtubetogo/)

```bash
    pip install youtubetogo
```

### Project 

You can install the package using pip from the source directory:

``bash
    git clone https://github.com/kdcllc/youtubetogo
```
```bash
    pip install .
```

## Command Line Usage

```bash
    youtubetogo -u <video_url> [-a]

    # YouTube Data API v3 api key is required
    # store the key in .env file use .env.sample file
    youtubetogo -c <channel_id> [-a]
```

```bash
python main.py -u <video_url> [-a]
python main.py -c <channel_id> [-a]
```

### Arguments

- `-a`, `--audio`: Convert videos to audio
- `-u`, `--url`: URL of the video to download and convert
- `-c`, `--channel`: Channel ID to download and convert videos from

## Deploy

```bash
pip install build twine
```

```bash
python -m build
twine upload dist/*
```

