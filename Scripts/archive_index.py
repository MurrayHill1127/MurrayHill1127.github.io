import sqlite3
import os
import shutil
from datetime import datetime

db_path = '../.meta.db'

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_meta_data(article_type):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = f"""
    SELECT title, date, topic, link
    FROM blog
    WHERE type = ?
    ORDER BY date DESC, id DESC
    """ 
    cursor.execute(query, (article_type,))
    articles = cursor.fetchall()

    conn.close()
    return articles

def operate_index(article_type):
    all_meta_data = get_meta_data(article_type)

    navbar_path = '../Template/' + article_type + '_archive.html'
    footer_path = '../Template/archive_footer.html'
    navbar_content = read_file(navbar_path)
    footer_content = read_file(footer_path)

    table_content = ''
    for meta_data in all_meta_data:
        title = meta_data['title']
        date = meta_data['date']
        topic = meta_data['topic']
        link = meta_data['link']

        date_obj = datetime.strptime(date, '%Y%m%d')
        date = date_obj.strftime('%-m/%-d/%Y')

        table_content += f""" 
            <tr>
                <td><a href={link}>{title}</a></td>
                <td class="date">{date}</td>
                <td>{topic}</td>
            </tr>"""

    index_path = f'../{article_type}/archive.html' 
    with open(index_path, 'w', encoding='utf-8') as file:
        file.write(navbar_content)
        file.write(table_content)
        file.write(footer_content)

if __name__ == '__main__':
    operate_index('blog')
    operate_index('note')
    operate_index('writeup')
