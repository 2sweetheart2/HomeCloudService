import os

from flask import Flask, g

from cloud.cloud import main_cloud_page, cloud
from config import *
from settings.settings import main_settings_page, sett
from utils import utils_data, get_directory_structure

app = Flask(__name__, static_url_path='')
app.register_blueprint(sett)
app.register_blueprint(cloud)


@app.before_request
def before_request():
    g.con = sqlite3.connect('home_service.db')


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'con'):
        g.con.close()


@app.route('/')
def index_path():
    f = con.is_init(g.con)
    if f:
        return main_settings_page()
    else:
        g.con.close()
        g.con = sqlite3.connect('home_service.db')
        g.settings = con.get_settings(g.con)
        return main_cloud_page()


if __name__ == '__main__':
    utils_data['dirs'] = get_directory_structure(os.getcwd())
    app.run('0.0.0.0', 8200, debug=False)
