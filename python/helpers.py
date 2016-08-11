def search(path, ext):
    file_list = []
    for root, dirs, files in os.walk(path):
        file_list.extend([os.path.join(root, f) for f in files if f.lower().endswith(ext)])
    return sorted(file_list)
