import base64
import os

from flask import Blueprint, render_template, request, jsonify, g, send_file

from config import con

cloud = Blueprint('cloud', __name__, template_folder='templates')

images_formats = ['png', 'gif', 'jpg', 'jpeg']


def get_paths(rootdir):
    dir_structure = []

    try:
        for item in os.listdir(rootdir):

            item_path = os.path.join(rootdir, item)
            if os.path.isdir(item_path):
                dir_structure.append({'name': item_path.split('\\')[-1], 'type': 'folder'})
            else:
                format = item.split('.')[-1]
                if format in images_formats:
                    l = base64.b64encode(f'{rootdir}\\{item}'.split('\\')[-1].encode('utf-8')).decode('utf-8')
                    links.update({f'/load/{l}': f'{rootdir}\\{item}'})
                    dir_structure.append({'name': item, 'type': 'image', 'format': format, 'url': f'/load/{l}'})
                else:
                    dir_structure.append({'name': item, 'type': 'file', 'format': format})
    except PermissionError:
        pass
    return dir_structure


@cloud.route('/create-folder', methods=['POST'])
def create_folder():
    add_path = '\\'.join(request.json['path'])

    rootdir = con.get_settings(g.con)['path'] + add_path

    if not os.path.exists(rootdir + "\\" + request.json['folder']):
        os.makedirs(rootdir + "\\" + request.json['folder'])
    d = get_paths(rootdir)
    return jsonify(files=d)


@cloud.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'Нет файла для загрузки'}), 400

    add_path = request.values['path']

    rootdir = con.get_settings(g.con)['path']
    if len(add_path) != 0:
        rootdir += f'{add_path}'

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'Файл не выбран'}), 400

    file_path = os.path.join(rootdir, file.filename)
    file.save(file_path)

    d = get_paths(rootdir)
    return jsonify(files=d)


links = {}


@cloud.route('/get_link', methods=['POST'])
def get_file_link():
    add_path = '\\'.join(request.json['path'])
    rootdir = con.get_settings(g.con)['path']

    if len(add_path) != 0:
        rootdir += f'\\{add_path}'
    rootdir += f'\\{request.json["name"]}'
    l = base64.b64encode(rootdir.split('\\')[-1].encode('utf-8')).decode('utf-8')
    links.update({f'/load/{l}': rootdir})
    return jsonify({'url': f'/load/{l}'})


@cloud.route('/load/<path>', methods=["GET"])
def load_files(path):
    l = links.pop(f'/load/{path}')
    return send_file(l, as_attachment=True, )


@cloud.route('/files', methods=['POST'])
def get_files():
    add_path = '\\'.join(request.json['path'])
    rootdir = con.get_settings(g.con)['path']

    if len(add_path) != 0:
        rootdir += f'\\{add_path}'
    d = get_paths(rootdir)

    # d = utils.get_directory_structure(g.settings['path'])
    print(d)
    return jsonify(files=d)


def main_cloud_page():
    return render_template('cloud.html')
