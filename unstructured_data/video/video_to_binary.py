import base64
import json
import subprocess
import os

# Path to your video in HDFS
hdfs_path_to_video = '/user/csso_adrian.muhammad/videos/example_video.mp4'

# Temporary local file path for the video
local_path_to_video = '/tmp/video_temp.mp4'

# Use subprocess to execute the hdfs dfs -get command to download the video from HDFS
subprocess.run(['hdfs', 'dfs', '-get', hdfs_path_to_video, local_path_to_video], check=True)

# Open the local video file in binary mode
with open(local_path_to_video, "rb") as video_file:
    # Read the video file and encode it to base64
    encoded_string = base64.b64encode(video_file.read()).decode('utf-8')

# Create a semi-structured JSON object with the base64 encoded video
video_data = {
    "filename": os.path.basename(hdfs_path_to_video),
    "filetype": "video/mp4",  # Correct MIME type for an MP4 video
    "video_base64": encoded_string
}

# Convert the JSON object to a string
json_data = json.dumps(video_data, indent=4)

# Name of the JSON file to be saved in HDFS, derived from the video file name
json_file_path = os.path.splitext(hdfs_path_to_video)[0] + '_binary.json'

# Save the JSON data to a local file first
local_json_file_path = '/tmp' + os.path.basename(json_file_path)
with open(local_json_file_path, 'w') as json_file:
    json_file.write(json_data)

# Use subprocess to execute the hdfs dfs -put command to upload the JSON to HDFS
subprocess.run(['hdfs', 'dfs', '-put', local_json_file_path, json_file_path], check=True)

print(f"JSON data saved as {json_file_path} in HDFS")

# Optionally, delete the temporary local files to clean up
os.remove(local_path_to_video)
os.remove(local_json_file_path)