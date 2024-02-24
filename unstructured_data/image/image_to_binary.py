import base64
import json
import subprocess
from PIL import Image
import io
import os

# Path to your image in HDFS
hdfs_path_to_image = '/user/csso_adrian.muhammad/images/example_image.jpg'

# Temporary local file path
local_path_to_image = '/tmp/image_temp.jpg'

# Use subprocess to execute the hdfs dfs -get command
subprocess.run(['hdfs', 'dfs', '-get', hdfs_path_to_image, local_path_to_image], check=True)

# Open the local image file
with open(local_path_to_image, "rb") as image_file:
    # Read the image file in binary mode
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

# Create a semi-structured JSON object with the base64 encoded image
image_data = {
    "filename": os.path.basename(hdfs_path_to_image),
    "filetype": "image/jpeg",  # Change to the correct mime type if not jpeg
    "image_base64": encoded_string
}

# Convert the JSON object to a string
json_data = json.dumps(image_data, indent=4)

# Name of the JSON file to be saved in HDFS
json_file_path = os.path.splitext(hdfs_path_to_image)[0] + '_binary.json'

# Save the JSON data to a local file first
local_json_file_path = '/tmp' + os.path.basename(json_file_path)
with open(local_json_file_path, 'w') as json_file:
    json_file.write(json_data)

# Use subprocess to execute the hdfs dfs -put command
subprocess.run(['hdfs', 'dfs', '-put', local_json_file_path, json_file_path], check=True)

print(f"JSON data saved as {json_file_path} in HDFS")

# Optionally, delete the temporary local files
os.remove(local_path_to_image)
os.remove(local_json_file_path)