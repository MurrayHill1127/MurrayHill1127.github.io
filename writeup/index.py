import os
import re
from datetime import datetime

# 获取脚本所在目录
script_dir = os.path.dirname(__file__)

# 设置数据目录
archive_dir = os.path.join(script_dir, 'all')

# 生成 HTML 索引文件的路径
index_file_path = os.path.join(script_dir, 'archive.html')

# 正则表达式模式
pattern = re.compile(r'(\d{2})(\d{2})_(.*?)_(.*?).html')

def generate_index():
    html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
    <head>
        <title>Murray Hill</title>
        <meta http-equiv="Content-type" content="text/html; charset=utf-8" />



        <link rel="stylesheet" type="text/css" href="../css/styles.css" />
		  <style>
            th
            {
                text-align: left;
            }
            td
            {
                vertical-align: bottom;
            }
            td.date
            {
                padding-left: 5px;
                padding-right: 5px;
            }
        </style>
   </head>

    <body>
        <header>
            <h1><a class="header-link" href="../index.html">Murray Hill</a></h1>

            <nav>
                <div class="nav">
                    <a class="nav-link" href="../blog/archive.html">Blog</a>
                    <a class="nav-link-current" href="../writeup/archive.html">WriteUp</a>
                    <a class="nav-link" href="../about/about.html">About</a>
                </div>
            </nav>

		    <hr />
			<nav>
                <div class="nav">
                    <a class="nav-link-current" href='../blog/archive.html'>Archive</a>
                    <a class="nav-link" href="../blog/category.html">Category</a>
                </div>
            </nav>
        </header>

		 <hr />
        <table>
            <thead>
                <tr>
					<th>Title</th>
                    <th>Date</th>
                    <th>Subject</th>
                </tr>
            </thead>
            <tbody>
    """

    entries = []

    for folder_name in os.listdir(archive_dir):
        folder_path = os.path.join(archive_dir, folder_name)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                match = pattern.match(file_name)
                if match:
                    month, day, title, subject = match.groups()
                    title = title.replace('-', ' ')
                    subject = subject
                    date = f"20{folder_name[:2]}-{month}-{day}"
                    file_path = os.path.join("./all/"+folder_name, file_name)
                    entries.append((date, title, subject, file_path))

    # 按日期排序
    entries.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'), reverse=True)

    for entry in entries:
        date, title, subject, file_path = entry
        html_content += f"""
            <tr>
                <td><a href="{file_path}">{title}</a></td>
                <td class="date">{date}</td>
                <td>{subject}</td>
            </tr>
        """

    html_content += """
		</tbody>
		</table>

		<hr />
        <footer>
            &copy; 2024, Murray Hill 
        </footer>
    </body>
</html>
    """

    # 写入 HTML 文件
    with open(index_file_path, 'w') as file:
        file.write(html_content)
    print(f"索引已生成: {index_file_path}")

if __name__ == "__main__":
    generate_index()
