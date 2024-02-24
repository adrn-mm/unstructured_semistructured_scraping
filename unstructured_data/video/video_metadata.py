from moviepy.editor import VideoFileClip
import json
import subprocess
import os

def video_to_json(video_path):
    with VideoFileClip(video_path) as clip:
        video_info = {
            "filename": os.path.basename(video_path),
            "duration": clip.duration,
            "width": clip.size[0],
            "height": clip.size[1],
            "fps": clip.fps
        }
        return json.dumps(video_info)

# Lokasi video di HDFS dan lokal
hdfs_video_path = '/user/csso_adrian.muhammad/videos/example_video.mp4'
local_video_path = '/tmp/example_video.mp4'

# Salin video dari HDFS ke lokal
subprocess.run(['hadoop', 'fs', '-get', hdfs_video_path, local_video_path], check=True)

# Proses metadata video
video_json = video_to_json(local_video_path)

# Lokasi dan nama file metadata JSON di HDFS
hdfs_directory_path = '/user/csso_adrian.muhammad/videos'
formatted_file_path = '/tmp/example_video_metadata.json'
hdfs_file_name = 'example_video_metadata.json'

try:
    with open(formatted_file_path, 'w') as formatted_file:
        formatted_file.write(video_json + '\n')  # Menulis JSON ke file

    # Unggah metadata JSON ke HDFS
    subprocess.call(['hadoop', 'fs', '-mkdir', '-p', hdfs_directory_path])
    subprocess.call(['hadoop', 'fs', '-put', '-f', formatted_file_path, f"{hdfs_directory_path}/{hdfs_file_name}"])
    print("File JSON berhasil di-upload ke HDFS.")

    # Buat tabel eksternal Hive untuk metadata
    hive_query = f"""
    CREATE EXTERNAL TABLE IF NOT EXISTS video_metadata (
        filename STRING,
        duration FLOAT,
        width INT,
        height INT,
        fps FLOAT
    )
    ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
    STORED AS TEXTFILE
    LOCATION '{hdfs_directory_path}';
    """
    subprocess.run(['hive', '-e', hive_query], check=True)
    print("External table berhasil dibuat di Hive.")

finally:
    # Bersihkan file sementara lokal
    os.remove(local_video_path)
    os.remove(formatted_file_path)