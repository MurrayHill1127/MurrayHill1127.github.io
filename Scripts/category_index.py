import pdb
import sqlite3
import os
import shutil
from collections import defaultdict

db_path = '../.meta.db'

script_tag = '\n<script src="/script/script.js"></script>'

folder_string = '''
<li>
<div class="folder">
    <div class="folder-name">
        <img src="/image/folder.gif" alt="Folder" class="icon">{}
    </div>
    <ul class="hidden">
        <li>
            {}
        </li>
    </ul>
</div>
</li>
'''

root_folder_string = '''
<div class="folder">
    <div class="folder-name">
        <img src="/image/folder.gif" alt="Folder" class="icon">{}
    </div>
    <ul class="hidden">
        <li>
            {}
        </li>
    </ul>
</div>
'''

text_string = '''
<li>
    <img src="/image/text.gif" alt="File" class="icon">
    <a href="{}">{}</a>
</li>
'''

file_system = '''
<div id="file-system">
    {}
</div>
'''

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_meta_data(article_type):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = f"""
    SELECT title, date, topic, link, category, filename
    FROM blog
    WHERE type = ?
    ORDER BY date ASC 
    """ 
    cursor.execute(query, (article_type,))
    articles = cursor.fetchall()

    conn.close()
    return articles

def generate_tree(all_meta_data):
    tree = defaultdict(lambda: defaultdict(dict))

    for meta_data in all_meta_data:
        title = meta_data['title']
        filename = meta_data['filename']
        category = meta_data['category']
        link = meta_data['link']

        parts = category.split('/')[:-1]
        current_level = tree

        for part in parts:
            if part not in current_level:
                current_level[part] = {'type': 'folder', 'children': {}}
            current_level = current_level[part]['children']
        
        current_level[filename] = {'type': 'file', 'title':title, 'link': link}

    return tree
      

def get_children(node, level):
    children = ''
    for key in node:
       if node[key]['type'] == 'file':
            children += text_string.format(node[key]['link'], node[key]['title'])

    if level == 0:
        for key in node:
            if node[key]['type'] == 'folder':
                children += root_folder_string.format(key, get_children(node[key]['children'], level+1))
    else:
        for key in node:
            if node[key]['type'] == 'folder':
                children += folder_string.format(key, get_children(node[key]['children'], level+1))

    return children

def get_main_content(all_meta_data):
    tree = generate_tree(all_meta_data)
    main_content = get_children(tree, 0)

    return main_content

def operate_index(article_type):
    all_meta_data = get_meta_data(article_type)

    navbar_path = '../Template/' + article_type + '_category.html'
    footer_path = '../Template/main_footer.html'
    navbar_content = read_file(navbar_path)
    footer_content = read_file(footer_path)

    main_content = get_main_content(all_meta_data)
    category_content = file_system.format(main_content)

    index_path = f'../{article_type}/category.html' 
    with open(index_path, 'w', encoding='utf-8') as file:
        file.write(navbar_content)
        file.write(category_content)
        file.write(script_tag)
        file.write(footer_content)

if __name__ == '__main__':
    operate_index('blog')
    operate_index('note')
    operate_index('writeup')
