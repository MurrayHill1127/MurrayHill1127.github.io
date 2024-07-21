import os
import markdown2

def convert_markdown_to_html(directory, count):
    navbar_html = """
<!DOCTYPE html>
<html lang="zh-CN">
    <head>
        <title>Murray Hill</title>
        <meta http-equiv="Content-type" content="text/html; charset=utf-8" />



        <link rel="stylesheet" type="text/css" href="../../../css/styles.css" />
  </head>

    <body>
        <header>
            <h1><a class="header-link" href="../../../index.html">Murray Hill</a></h1>

            <nav>
                <div class="nav">
                    <a class="nav-link-current" href="../../../blog/archive.html">Blog</a>
                    <a class="nav-link" href="../../../writeup/archive.html">WriteUp</a>
                    <a class="nav-link" href="../../../about/about.html">About</a>
                </div>
            </nav>

		    <hr />
			<nav>
                <div class="nav">
                    <a class="nav-link-current" href='../../../blog/archive.html'>Archive</a>
                    <a class="nav-link" href="../../../blog/category.html">Category</a>
                </div>
            </nav>
        </header>
        <hr />
"""

    end_html = """
        <hr />
        <footer>
            &copy; 2024, Murray Hill 
        </footer>
    </body>
</html>
""" 
    # 遍历目录中的所有文件
    for file_name in os.listdir(directory):
        if file_name.endswith('.md'):

            # 构建 Markdown 文件的完整路径
            markdown_file_path = os.path.join(directory, file_name)

            # 构建输出 HTML 文件的路径
            html_file_name = file_name.replace('.md', '.html')
            html_file_path = os.path.join(directory, html_file_name)

            # 读取 Markdown 文件内容
            with open(markdown_file_path, 'r', encoding='utf-8') as md_file:
                markdown_content = md_file.read()

            # 使用 markdown2 将 Markdown 转换为 HTML
            html_content = markdown2.markdown(markdown_content)

            # 将 HTML 内容写入文件
            with open(html_file_path, 'w', encoding='utf-8') as html_file:
                html_file.write(navbar_html)
                html_file.write(html_content)
                html_file.write(end_html)
            
            count += 1
            print(f"{count}: 已将 {file_name} 转换为 {html_file_name}")
    return count


if __name__ == "__main__":
    # 设置需要转换的目录
    count = 0
    target_directory = os.path.dirname(os.path.abspath(__file__))  # 当前目录
    target_directory = os.path.join(target_directory, 'all')
    for folder in os.listdir(target_directory):
        folder_path = os.path.join(target_directory, folder)
        if os.path.isdir(folder_path):
            count = convert_markdown_to_html(folder_path, count)
