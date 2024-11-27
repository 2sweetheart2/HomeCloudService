import os

utils_data = {}

dirs = {}


def get_directory_structure(rootdir):
    """
    Создает древовидную структуру каталогов в виде словаря.
    """
    if rootdir in dirs:
        return dirs[rootdir]
    dir_structure = {'name': os.path.basename(rootdir), 'path_like': rootdir.split('\\'), 'children': []}
    try:
        for item in os.listdir(rootdir):
            item_path = os.path.join(rootdir, item)
            if os.path.isdir(item_path):
                dir_structure['children'].append(get_directory_structure(item_path))
            else:
                dir_structure['children'].append({'name': item})
    except PermissionError:
        pass
    dirs.update({rootdir: dir_structure})
    return dir_structure
