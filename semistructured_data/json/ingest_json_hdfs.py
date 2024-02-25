import subprocess
import json
import os

# Lokasi file JSON lokal
local_file_path = 'dummy.json'

# Lokasi file JSON yang sudah diformat
formatted_file_path = 'formatted_dummy.json'

# Lokasi target di HDFS (pastikan ini adalah direktori, bukan file)
hdfs_directory_path = '/user/csso_andrew/json'
# Nama file di HDFS, dapat menggunakan nama file asli atau yang sudah diformat
hdfs_file_name = 'dummy.json'

# Langkah 1 & 2: Membaca dan mengubah format file JSON
with open(local_file_path, 'r') as json_file:
     json_data = json.load(json_file)

with open(formatted_file_path, 'w') as formatted_file:
     for entry in json_data:
        json.dump(entry, formatted_file)
        formatted_file.write('\n')

# Langkah 3: Mengunggah file yang sudah diformat ke HDFS
# Pastikan direktori target sudah ada atau buat menggunakan 'hdfs dfs -mkdir'
subprocess.call(['hadoop', 'fs', '-mkdir', '-p', hdfs_directory_path])
subprocess.call(['hadoop', 'fs', '-put', '-f', formatted_file_path, f"{hdfs_directory_path}/{hdfs_file_name}"])

os.remove(formatted_file_path)

print("File JSON yang sudah diformat berhasil di-upload ke HDFS.")