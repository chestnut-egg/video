import os
import shutil

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
    return redirect("/index")

@app.route('/video')
def video():
    info = {}
    the_video_name = request.args.get('video_name')
    the_root = request.args.get('root')
    url = the_root + the_video_name
    logger.info('in:' + str(url))
    copy(url,"/home/ppg/PycharmProjects/video/static/"+the_video_name)
    info["video_url"] = "/static/"+the_video_name
    return render_template('video.html',info = info)

@app.route('/index',methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        root = request.args.get('root')
        if root == None:
            logger.info('root: null')
        else:
            logger.info('root:' + root)
        if root == None:
            info = nowos(cp.get("file", "download_address"))
            return render_template('index.html', info=info)
        else:
            info = nowos(root)
            return render_template('index.html', info=info)

    info = nowos(cp.get("file","download_address"))
    return render_template('index.html',info = info)



# @app.route("/hello/<username>")
# def hello_user(username):
#   return "Hello {}!".format(username)

def nowos(file_dir):

    logger.info('listdir'+str(os.listdir(file_dir)))

    files = []
    dirs_name = []
    dirs_url = []
    root = file_dir

    for name in os.listdir(file_dir):
        if os.path.isfile(os.path.join(root, name)):
            files.append(name)
        else:
            dirs_name.append(name)
            dirs_url.append(os.path.join(root, name))

    logger.info('files:' + str(files))

    str1 = str(cp.get("file","video"))
    allow = str1.split(",")

    video_name = []
    video_url = []

    for file_name in files:
        if os.path.splitext(file_name)[1] in allow:
            video_name.append(file_name)
            video_url.append(os.path.join(root,file_name))

    logger.info('video_name:'+ str(video_name))

    dirs_info ={}

    for i in range(0,len(dirs_name)):
        dirs_info[dirs_name[i]] = dirs_url[i]


    info = {}
    info['root'] = root
    info['files'] = files
    info['dirs_name'] = dirs_name
    info['dirs_url'] = dirs_url
    info['dirs_info'] = dirs_info
    info['video_name'] = video_name
    info['video_url'] = video_url

    return info


def move(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        logger.info("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.move(srcfile, dstfile)
        logger.info("move %s -> %s" % (srcfile, dstfile))

def copy(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        logger.info("%s not exist!" % (srcfile))
    else:
        fpath,fname=os.path.split(dstfile)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.copyfile(srcfile,dstfile)
        logger.info("copy %s -> %s" % (srcfile, dstfile))


if __name__ == '__main__':
    app.run(debug=True)
