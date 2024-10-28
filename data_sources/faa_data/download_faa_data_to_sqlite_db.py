import csv
import sqlite3
import re
import os
import requests
import zipfile
import shutil

def clean_identifier(identifier):
    identifier = identifier.replace(' ', '_').replace('-', '_')
    identifier = re.sub(r'\W+', '', identifier)
    identifier = identifier.lstrip('\ufeff')  # Remove BOM if present
    return identifier


def download_and_unzip(url, tmp_dir):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    zip_file_path = os.path.join(tmp_dir, 'downloaded.zip')

    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(zip_file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(tmp_dir)

    os.remove(zip_file_path)

def create_db_from_csv(csv_file_paths, db_file_path):
    if os.path.exists(db_file_path):
        os.remove(db_file_path)
        
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    for csv_file_path in csv_file_paths:
        base_name = os.path.basename(csv_file_path)
        table_name = clean_identifier(os.path.splitext(base_name)[0])

        with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            original_headers = next(reader)
            headers = [clean_identifier(header) for header in original_headers]

            columns = ', '.join([f'"{header}" TEXT' for header in headers])
            create_table_sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns})'
            cursor.execute(create_table_sql)

            placeholders = ', '.join(['?'] * len(headers))
            insert_sql = f'INSERT INTO "{table_name}" VALUES ({placeholders})'
            for row in reader:
                cursor.execute(insert_sql, row)

    conn.commit()
    conn.close()

def cleanup_dir(directory):
    shutil.rmtree(directory)

# URL of the zip file and temp directory
url = 'https://registry.faa.gov/database/ReleasableAircraft.zip'
tmp_dir = './tmp_download'

# Download and unzip
download_and_unzip(url, tmp_dir)

# Specify the files you're interested in
interested_files = [
    'MASTER.txt',
    'ACFTREF.txt',
    'ENGINE.txt',
]

# Build paths for the interested files
csv_file_paths = [os.path.join(tmp_dir, filename) for filename in interested_files]

# Specify the database file path and create the database
db_file_path = 'plane_info.db'
create_db_from_csv(csv_file_paths, db_file_path)

# Cleanup the temporary directory
cleanup_dir(tmp_dir)

print("Process completed successfully.")
