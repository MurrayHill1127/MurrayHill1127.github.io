import os

def ensure_keep_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        
        if not any(os.scandir(root)):
            continue

        keep_file_path = os.path.join(root, '.keep')
        if not os.path.exists(keep_file_path):
            with open(keep_file_path, 'w') as keep_file:
                keep_file.write('This file is kept for avoiding GitHub Pages zipping directories without files.\n')
            print(f"Created .keep file: {keep_file_path}")

if __name__ == "__main__":
    ensure_keep_files('../')
