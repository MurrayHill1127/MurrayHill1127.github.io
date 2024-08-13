import os
import shutil  
import sqlite3
import markdown2
import re
from datetime import datetime

db_path = '../.meta.db'

def get_meta_data():
    conn = sqlite3.connect(db_path)

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM blog ORDER BY id DESC LIMIT 1')
    latest_entry = cursor.fetchone()

    conn.close()
    return latest_entry

def get_navbar_html(meta_data):
    navbar_path = '../Template/'
    navbar_file = meta_data['type'].lower() + '_main_navbar.html'
    navbar_path += navbar_file
    with open(navbar_path, 'r', encoding='utf-8') as navbar:
        navbar_html = navbar.read()
    return navbar_html

def get_footer_html(meta_data):
    footer_path = '../Template/main_footer.html'
    with open(footer_path, 'r', encoding='utf-8') as footer:
        footer_html = footer.read()
    return footer_html

def get_tdl_html(meta_data):
    title = meta_data['title']
    raw_date = meta_data['date']
    location = meta_data['location'] 

    date_obj = datetime.strptime(raw_date, "%Y%m%d")
    date = date_obj.strftime("%B %d, %Y")
    
    html_template = '''
    <h2 style="text-align: center;">{title}</h2>
    <p class="right">{date}<br />{location}</p>
    '''
    html_content = html_template.format(title=title, date=date, location=location)
    return html_content

def get_main_md(meta_data):
    md_path = '../Entry/' + meta_data['filename'] + '.md'

    with open(md_path, 'r', encoding='utf-8') as file:
        content = file.read()
 
    start = content.find('---')
    if start == -1:
        raise ValueError("Error: md2html.py YAML front matter not found")
    start += 3
    end = content.find('---', start)
    if end == -1:
        raise ValueError("Error: md2html.py  End of YAML front matter not found")
    end += 3

    main_md = content[end:].strip()
    return main_md 

def convert_markdown_to_html(main_md):
    html_content = markdown2.markdown(main_md)
    return html_content           

def get_reference(main_md):
    link_pattern = re.compile(r'\[(.*?)\]\((.*?)\)') 
    links = re.findall(link_pattern, main_md)

    return links  

def create_attachment_table(cursor, table_name):
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        blog_id INTEGER,
        reference_name TEXT,
        filename TEXT,
        link TEXT
    )
    ''')

def insert_into_attachments(cursor, blog_id, blog_title, blog_type, reference_count):
    cursor.execute('''
    INSERT INTO attachments (blog_id, blog_title, blog_type, reference_count)
    VALUES (?, ?, ?, ?)
    ''', (blog_id, blog_title, blog_type, reference_count))
    return cursor.lastrowid

def update_blog_table(cursor, blog_id, attachment_id):
    cursor.execute('''
    UPDATE blog
    SET attachment_id = ?
    WHERE id = ?
    ''', (attachment_id, blog_id))

def insert_into_attachment_table(cursor, table_name, blog_id, references, directory):
    path = '/' + directory 
    for reference_name, filename in references:
        link = path + filename
        cursor.execute(f'''
        INSERT INTO {table_name} (blog_id, reference_name,filename, link)
        VALUES (?, ?, ?, ?)
        ''', (blog_id, reference_name, filename, link))


def record_reference(meta_data, references):
    if not references:
        return
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    blog_id = meta_data['id']  
    blog_title = meta_data['title']
    blog_type = meta_data['type']
    reference_count = len(references)

    attachment_id = insert_into_attachments(cursor, blog_id, blog_title, blog_type, reference_count) 
    update_blog_table(cursor, blog_id, attachment_id) 
    
    table_name = f"attachment_{attachment_id}"
    create_attachment_table(cursor, table_name) 
    insert_into_attachment_table(cursor, table_name, blog_id, references, meta_data['directory'])

    conn.commit()
    conn.close()

def md2html():
    meta_data = get_meta_data()
    navbar_html = get_navbar_html(meta_data)
    footer_html = get_footer_html(meta_data)
    tdl_html = get_tdl_html(meta_data)
    main_md = get_main_md(meta_data) 
    main_html = convert_markdown_to_html(main_md)

    html_filename = meta_data['filename'] + '.html'
    html_path = '../Entry/' + html_filename

    with open(html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(navbar_html)
        html_file.write(tdl_html)
        html_file.write(main_html)
        html_file.write(footer_html)

    references = get_reference(main_md)
    record_reference(meta_data, references)

def get_attachment_data(attachment_id):
    table_name = f"attachment_{attachment_id}"

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM {table_name}')
    attachment_data = cursor.fetchall()
    conn.close()
    return attachment_data

def put_in_place():
    meta_data = get_meta_data()
    
    md_filename = meta_data['filename'] + '.md'
    html_filename = meta_data['filename'] + '.html'
    md_old_path = '../Entry/' + md_filename
    html_old_path = '../Entry/' + html_filename

    md_new_path = '../' + meta_data['directory'] 
    html_new_path = '../' + meta_data['directory']
    os.makedirs(md_new_path, exist_ok=True)
    os.makedirs(html_new_path, exist_ok=True)

    md_new_path += md_filename
    html_new_path += html_filename
    shutil.move(md_old_path, md_new_path)
    shutil.move(html_old_path, html_new_path)
    
    if meta_data['attachment_id'] == 0:
        return

    attachment_data = get_attachment_data(meta_data['attachment_id'])
    for attachment in attachment_data:
        filename = attachment['filename']
        old_path = '../Entry/' + filename

        if not os.path.isfile(old_path):
            continue

        new_path = '..' + attachment['link']
        shutil.move(old_path, new_path) 

if __name__ == "__main__":
    md2html()
    put_in_place()

