import sqlite3

conn = sqlite3.connect('../.meta.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS blog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT NOT NULL,
    location TEXT NOT NULL,
    type TEXT NOT NULL,
    topic TEXT NOT NULL,
    category TEXT NOT NULL,
    filename TEXT NOT NULL,
    directory TEXT NOT NULL,
    link TEXT NOT NULL,
    attachment_id INTEGER NOT NULL DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS attachments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    blog_id INTEGER NOT NULL,
    blog_title TEXT NOT NULL,
    blog_type TEXT NOT NULL,
    reference_count INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (blog_id) REFERENCES blog (id)
    )
''')

conn.commit()
conn.close()
