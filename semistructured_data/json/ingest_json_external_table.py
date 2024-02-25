import subprocess
  
hdfs_directory_path = '/user/csso_andrew/json'

# Langkah 4: Membuat external table di Hive
hive_query = f"""
    CREATE EXTERNAL TABLE IF NOT EXISTS adrian_json_table (
        userId INT,
        name STRING,
        age INT,
        email STRING,
        isSubscriber BOOLEAN
    )
    ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
    STORED AS TEXTFILE
    LOCATION '{hdfs_directory_path}';
    """
hive_cmd = ['hive', '-e', hive_query]

subprocess.run(hive_cmd, check=True)
print("External table berhasil dibuat di Hive.")