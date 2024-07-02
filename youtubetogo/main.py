"""
This script downloads and converts YouTube videos to either video or audio format.
It can download videos from a specific channel or a single video URL.

Dependencies:
- requests
- csv
- os
- asyncio
- subprocess
- argparse
- pytube
- dotenv

Usage:
    python main.py -u <video_url> [-a]
    python main.py -c <channel_id> [-a]

Arguments:
    -a, --audio: Convert videos to audio
    -u, --url: URL of the video to download and convert
    -c, --channel: Channel ID to download and convert videos from

Functions:
    create_csv_file(csv_file_path, key, channel):
        Create a CSV file containing video titles and URLs from a YouTube channel.

    convert_files(input_directory, output_directory, input_extension, output_extension, conversion_command):
        Convert all files in a directory from one format to another.

    download_video_from_url(video_url: str, video_output_path='') -> str:
        Download and convert a YouTube video from a URL.

    download_videos_from_channel(csv_file_path, video_output_path):
        Download and convert YouTube videos from a channel using a CSV file.

    main():
        Main function to parse arguments and initiate download and conversion.
"""

import requests
import csv
import os
import asyncio
import subprocess
import argparse
from pytube import YouTube
from pytube.cli import on_progress

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Set the key used to query the YouTube API
# https://console.cloud.google.com/apis/
key = os.environ.get('YOUTUBE_API_KEY')
# Specify the name of the channel to query - remember to drop the leading @ sign
channel = os.environ.get('YOUTUBE_CHANNEL_ID')

# Set the location of the CSV file to write to
csv_file_path = f"{channel}.csv"

def create_csv_file(csv_file_path, key, channel):
    """
    Create a CSV file containing video titles and URLs from a YouTube channel.

    Args:
        csv_file_path (str): The path to the CSV file to create.
        key (str): The YouTube API key.
        channel (str): The YouTube channel ID or username.
    """
    try:
        # Retrieve the channel id from the username (channel variable) - which is required to query the videos contained within a channel
        url = "https://youtube.googleapis.com/youtube/v3/channels?forUsername=" + channel + "&key=" + key
        request = requests.get(url)
        channelid = request.json()["items"][0]["id"]

    except:
        # if this fails, perform a channel search instead. Further documentation on this: https://developers.google.com/youtube/v3/guides/working_with_channel_ids
        url = "https://youtube.googleapis.com/youtube/v3/search?q=" + channel + "&type=channel" + "&key=" + key
        request = requests.get(url)
        channelid = request.json()["items"][0]["id"]["channelId"]

    # Create the playlist id (which is based on the channel id) of the uploads playlist (which contains all videos within the channel) - uses the approach documented at https://stackoverflow.com/questions/55014224/how-can-i-list-the-uploads-from-a-youtube-channel
    playlistid = list(channelid)
    playlistid[1] = "U"
    playlistid = "".join(playlistid)

    # Query the uploads playlist (playlistid) for all videos and writes the video title and URL to a CSV file (file path held in CSV variable)
    lastpage = "false"
    nextPageToken = ""

    while lastpage:
        videosUrl = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&playlistId=" + playlistid + "&pageToken=" + nextPageToken + "&maxResults=50" + "&fields=items(contentDetails(videoId%2CvideoPublishedAt)%2Csnippet(publishedAt%2Ctitle))%2CnextPageToken%2CpageInfo%2CprevPageToken%2CtokenPagination&key=" + key
        request = requests.get(videosUrl)
        videos = request.json()
        for video in videos["items"]:
            f = open(csv_file_path,"a")
            f.write(video["snippet"]["title"].replace(",","") + "," + "https://www.youtube.com/watch?v=" + video["contentDetails"]["videoId"] + "\n")
            f.close()
        try: # I'm sure there are far more elegant ways of identifying the last page of results!
            nextPageToken = videos["nextPageToken"]
        except:
            break

async def convert_files(input_directory, output_directory, input_extension, output_extension, conversion_command):
    """
    Convert all files in a directory from one format to another.

    Args:
        input_directory (str): The directory containing input files to convert.
        output_directory (str): The directory to save the converted files.
        input_extension (str): The extension of the input files.
        output_extension (str): The extension of the output files.
        conversion_command (str): The command to use for conversion.
    """
    input_files = [f for f in os.listdir(input_directory) if f.endswith(input_extension)]
    tasks = []
    for input_file in input_files:
        input_path = os.path.join(input_directory, input_file)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        output_path = os.path.join(output_directory, os.path.splitext(input_file)[0] + output_extension)
        command = conversion_command.format(input_path=input_path, output_path=output_path)
        tasks.append(asyncio.to_thread(subprocess.call, command, shell=True))
    await asyncio.gather(*tasks)
    print(f"All {input_extension} files have been converted to {output_extension} format.")

async def download_video_from_url(video_url: str, video_output_path='') -> str:
    """
    Download and convert a YouTube video from a URL.

    Args:
        video_url (str): The URL of the video to download.
        download_type (str): The type of download ("video" or "audio").
    """
    yt = YouTube(video_url, on_progress_callback=on_progress)
    stream = yt.streams.get_highest_resolution()
    video_file_path = os.path.join(video_output_path, stream.default_filename)

    if video_output_path =='':
        video_output_path = f'videos-{yt.video_id}'
        video_file_path = os.path.join(video_output_path, stream.default_filename)
    
    if not os.path.exists(video_file_path):
        await asyncio.to_thread(stream.download, output_path=video_output_path)
        print(f"Downloaded {video_url} as video")
    else:
        print(f"Video {video_url} already exists, skipping download")
    return yt.video_id, video_output_path

async def download_videos_from_channel(csv_file_path, video_output_path):
    """
    Download and convert YouTube videos from a channel using a CSV file.

    Args:
        csv_file_path (str): The path to the CSV file containing video URLs.
        download_type (str): The type of download ("video" or "audio").
    """

    tasks = []
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            video_url = row[1]  # Assuming the URL is the second column
            tasks.append(download_video_from_url(video_url, video_output_path))

    await asyncio.gather(*tasks)

# main
if __name__ == "__main__":
    async def main():
        """
        Main function to parse arguments and initiate download and conversion.
        """
        parser = argparse.ArgumentParser(description="Download and convert YouTube videos.")
        parser.add_argument('-a', '--audio', action='store_true', help="Convert videos to audio")
        parser.add_argument('-u', '--url', type=str, help="URL of the video to download and convert")
        parser.add_argument('-c', '--channel', type=str, help="Channel ID to download and convert videos from")
        args = parser.parse_args()

        download_type = 'audio' if args.audio else 'video'
        conversion_command = 'ffmpeg -y -i "{input_path}" "{output_path}"'

        if args.url:
            video_url = args.url
            id,video_output_path  = await download_video_from_url(video_url, '')
            audio_output_path = f"audios-{id}"

            if download_type == 'audio':
                await convert_files(video_output_path, audio_output_path, '.mp4', '.mp3', conversion_command)
        elif args.channel:
            if not key:
                raise ValueError("YouTube API key must be provided when a channel ID is specified.")
            channel = args.channel
            csv_file_path = f"{channel}.csv"
            print("Please provide either a video URL or a channel ID.")
            # check if the csv file exists
            if not os.path.exists(csv_file_path):
                create_csv_file(csv_file_path, key, channel)
            video_output_path = f"videos-{channel}"
            audio_output_path = f"audios-{channel}"
            await download_videos_from_channel(csv_file_path,video_output_path)
            if download_type == 'audio':
                await convert_files(video_output_path, audio_output_path, '.mp4', '.mp3', conversion_command)
        
    asyncio.run(main())
