import sqlite3
import yaml
import os
import sys

db_path = '../.meta.db'

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def insert_data(conn, data):
    sql = '''
    INSERT INTO blog (title, date, location, type, topic, category, filename, directory, link)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

def extract_metadata(md_file):
    with open(md_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    start = content.find('---')
    if start == -1:
        raise ValueError("Error: meta.py YAML front matter not found")
    start += 3
    end = content.find('---', start)
    if end == -1:
        raise ValueError("Error: meta.py  End of YAML front matter not found")
    
    yaml_content = content[start:end].strip()
    
    metadata = yaml.safe_load(yaml_content)
    return metadata

def generate_directory(typE, date, filename):
    year = date[:4]
    mm = date[4:6]
    mmdd = date[4:]

    directory = os.path.join(
        typE,
        year,
        mm,
        f"{mmdd}-{filename}"
    )
    directory = directory + "/"
    return directory


def main():
    if len(sys.argv) != 2:
        print("Error: meta.py len(sys.argv) != 2")
        sys.exit(1) 
    md_file = '../Entry/' + sys.argv[1]
    
    conn = create_connection(db_path) 

    metadata = extract_metadata(md_file)
    base_name, ext = os.path.splitext(os.path.basename(md_file))
    directory = generate_directory(metadata['type'].lower(), metadata['date'], base_name)
    link = "/" + directory + base_name + ".html"

    data = (
        metadata['title'],
        metadata['date'],
        metadata['location'],
        metadata['type'].lower(),
        metadata['topic'],
        metadata['category'],
        base_name,
        directory,
        link
    )
    
    insert_data(conn, data)

    conn.close()

if __name__ == '__main__':
    main()
