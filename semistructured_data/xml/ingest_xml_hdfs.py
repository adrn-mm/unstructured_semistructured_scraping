import subprocess
import json
import xmltodict

# Lokasi file JSON lokal
local_file_path = 'dummy.xml'

# Lokasi file JSON yang akan dihasilkan setelah konversi
converted_json_path = 'converted_from_xml.json'

# Lokasi target di HDFS untuk file XML
hdfs_directory_path_xml = '/user/csso_adrian.muhammad/xml'
# Lokasi target di HDFS untuk file JSON
hdfs_directory_path_json = '/user/csso_adrian.muhammad/xml/converted_json'

# Nama file di HDFS, dapat menggunakan nama file asli atau yang sudah dikonversi
hdfs_file_name_xml = 'dummy.xml'
hdfs_file_name_json = 'converted_from_xml.json'

# Langkah 1: Mengunggah file XML ke HDFS
subprocess.call(['hadoop', 'fs', '-mkdir', '-p', hdfs_directory_path_xml])
subprocess.call(['hadoop', 'fs', '-put', '-f', local_file_path, f"{hdfs_directory_path_xml}/{hdfs_file_name_xml}"])
print("File XML berhasil di-upload ke HDFS.")