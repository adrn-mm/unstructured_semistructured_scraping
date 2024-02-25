from PIL import Image
import json
import os
import subprocess

def image_metadata(image_path):
    with Image.open(image_path) as img:
        image_info = {
            "filename": os.path.basename(image_path),
            "width": img.width,
            "height": img.height,
            "format": img.format
        }
        return json.dumps(image_info)  # Tanpa indentasi untuk format single-line

# Lokasi gambar di HDFS dan lokal
hdfs_image_path = '/user/csso_andrew/images/example_image.jpg'
local_image_path = '/tmp/example_image.jpg'

# Salin gambar dari HDFS ke lokal
subprocess.run(['hadoop', 'fs', '-get', hdfs_image_path, local_image_path], check=True)

# Proses metadata gambar
image_metadata_json = image_metadata(local_image_path)

# Lokasi dan nama file metadata JSON di HDFS
hdfs_directory_path = '/user/csso_andrew/images/'
formatted_file_path = '/tmp/example_image_metadata.json'
hdfs_file_name = 'example_image_metadata.json'

try:
    with open(formatted_file_path, 'w') as formatted_file:
        formatted_file.write(image_metadata_json + '\n')  # Tambahkan newline setelah objek JSON

    # Unggah metadata JSON ke HDFS
    subprocess.call(['hadoop', 'fs', '-mkdir', '-p', hdfs_directory_path])
    subprocess.call(['hadoop', 'fs', '-put', '-f', formatted_file_path, f"{hdfs_directory_path}/{hdfs_file_name}"])
    print("File JSON berhasil di-upload ke HDFS.")

    # Buat tabel eksternal Hive untuk metadata
    hive_query = f"""
    CREATE EXTERNAL TABLE IF NOT EXISTS image_metadata (
        filename STRING,
        width INT,
        height INT,
        format STRING
    )
    ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
    STORED AS TEXTFILE
    LOCATION '{hdfs_directory_path}';
    """
    subprocess.run(['hive', '-e', hive_query], check=True)
    print("External table berhasil dibuat di Hive.")

finally:
    # Bersihkan file sementara lokal
    os.remove(local_image_path)
    os.remove(formatted_file_path)