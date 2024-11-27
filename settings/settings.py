import os

from flask import Blueprint, render_template, request, jsonify, g, redirect

from config import con
from utils import get_directory_structure

sett = Blueprint('settings', __name__, template_folder='templates')


@sett.route('/settings/get_directory_structure', methods=['POST'])
def get_directory():
    path = request.values['path']
    if path == 'current':
        path = os.getcwd()
    dir_structure = get_directory_structure(path)
    return jsonify(dir_structure)


@sett.route('/settings/set', methods=['POST'])
def settings_set_language():
    con.apply_settings(**request.json, connection=g.con)
    return redirect('/')


def main_settings_page():
    return render_template('registration.html')
