import subprocess
import json
import xmltodict

# Lokasi file JSON lokal
xml_file_path = 'dummy.xml'

# Lokasi file JSON yang akan dihasilkan setelah konversi
converted_json_path = 'converted_from_xml.json'

# Lokasi target di HDFS untuk file XML
hdfs_directory_path_xml = '/user/csso_adrian.muhammad/xml'
# Lokasi target di HDFS untuk file JSON
hdfs_directory_path_json = '/user/csso_adrian.muhammad/xml/converted_json'

# Nama file di HDFS, dapat menggunakan nama file asli atau yang sudah dikonversi
hdfs_file_name_xml = 'dummy.xml'
hdfs_file_name_json = 'converted_from_xml.json'

with open(xml_file_path, 'r') as xml_file:
    xml_content = xml_file.read()
    json_data = xmltodict.parse(xml_content, attr_prefix='')  # Menghilangkan attr_prefix jika ada

    # Misalkan struktur XML memiliki root <catalog> yang berisi banyak <book>
    books = json_data.get('catalog', {}).get('book', [])

    # Pastikan 'books' adalah list untuk kasus hanya satu <book>
    if isinstance(books, dict):
        books = [books]

with open(converted_json_path, 'w') as json_file:
    for book in books:
        # Menulis setiap buku sebagai satu objek JSON per baris
        json_file.write(json.dumps(book) + '\n')

# Langkah 4: Mengunggah file JSON yang sudah dikonversi ke HDFS
subprocess.call(['hadoop', 'fs', '-mkdir', '-p', hdfs_directory_path_json])
subprocess.call(['hadoop', 'fs', '-put', '-f', converted_json_path, f"{hdfs_directory_path_json}/{hdfs_file_name_json}"])
print("File JSON yang sudah dikonversi berhasil di-upload ke HDFS.")

# Langkah 5: Membuat external table di Hive menggunakan file JSON
hive_query = f"""
USE poc;
CREATE EXTERNAL TABLE IF NOT EXISTS adrian_xml_table (
    id STRING,
    author STRING,
    title STRING,
    genre STRING,
    price STRING,
    publish_date STRING,
    description STRING
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
STORED AS TEXTFILE
LOCATION '{hdfs_directory_path_json}'
TBLPROPERTIES ('json.paths'='$.books[*]');
"""
hive_cmd = ['hive', '-e', hive_query]

subprocess.run(hive_cmd, check=True)
print("External table berhasil dibuat di Hive berdasarkan file JSON.")

subprocess.run(hive_cmd, check=True)
print("External table berhasil dibuat di Hive.")