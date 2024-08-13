import os

def remove_keep_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == '.keep':
                keep_file_path = os.path.join(root, file)
                os.remove(keep_file_path)
                print(f"Deleted .keep file: {keep_file_path}")

if __name__ == "__main__":
    remove_keep_files('../')
