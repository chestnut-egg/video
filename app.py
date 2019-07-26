import os
from flask import *
import logging
import configparser

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

cp = configparser.ConfigParser()
cp.read('myconfig.conf')


app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect(url_for(index))

@app.route('/index')
def index():
    info = nowos(cp.get("file","download_address"))
    return render_template('index.html',info = info)

def nowos(file_dir):

    logger.info(os.listdir(file_dir))

    files = []
    dirs = []
    root = file_dir

    for name in os.listdir(file_dir):
        if os.path.isfile(os.path.join(root, name)):
            files.append(name)
        else:
            dirs.append(name)

    logger.info(files)

    str1 = str(cp.get("file","video"))
    allow = str1.split(",")

    video_name = []
    video_url = []

    for file_name in files:
        if os.path.splitext(file_name)[1] in allow:
            video_name.append(file_name)
            video_url.append(os.path.join(root,file_name))

    logger.info(video_name)

    info = {}
    info['root'] = root
    info['files'] = files
    info['dirs'] = dirs
    info['video_name'] = video_name
    info['video_url'] = video_url

    return info


if __name__ == '__main__':
    app.run(debug=True)
