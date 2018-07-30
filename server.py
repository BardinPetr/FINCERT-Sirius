from utils.FrontendCallBack import FrontendCallBack
from utils.StoppableThread import StoppableThread
from utils.websocketserver import WebsocketServer
from werkzeug.utils import secure_filename
from flask import render_template, request
from STIX2Parse.Parse import parse_stix
from utils.nocache import nocache
from utils.encryption import *
from flask import Flask
from time import sleep
from Main import run
import webbrowser
import platform
import logging
import signal
import json
import os

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp')
ALLOWED_EXTENSIONS = {'json'}

app = Flask(__name__)
enc = EncryptedWay()
mainthread = None
callback = None
pre_stix = None
server = None

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def kill():
    os.kill(os.getpid(), signal.SIGTERM)
    os.kill(os.getpid(), signal.SIGKILL)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
@nocache
def index():
    global pre_stix
    try:
        if request.method == 'POST':
            if 'file' not in request.files:
                raise Exception("No file in request")
            file = request.files['file']
            if file.filename == '':
                raise Exception("File is not a file...")
            if file and allowed_file(file.filename):
                filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                file.save(filename)
                file.close()
                pre_stix = parse_stix(open(filename, 'r'))
        return render_template('index-black.html', disabled=(platform.system() != 'Windows'))
    except Exception as ex:
        return render_template('error.html', res=ex)


@app.route('/settings', methods=['GET', 'POST'])
@nocache
def settings():
    try:
        return render_template('settings-black.html', cred=get_cred())
    except Exception as ex:
        return render_template('error.html', res=ex)


@app.route('/faq', methods=['GET', 'POST'])
@nocache
def faq():
    try:
        return render_template('help_faq.html')
    except Exception as ex:
        return render_template('error.html', res=ex)


def ws_receive(meta, wss, txt):
    global mainthread, pre_stix
    print("Received by WS:", txt)
    if txt.startswith("NOTENC"):
        data = txt.split(':::')[1:]
        try:
            if data[0] == "START":
                data = json.loads(data[1])
                res = {}
                for name in data['used']:
                    cur = data[name]
                    if type(cur) == list:
                        res[name] = list(map(lambda x: x['norm'] if 'norm' in x else x, cur))
                    else:
                        res[name] = {}
                        for x, y in cur.items():
                            res[name][x] = list(map(lambda j: j['norm'] if 'norm' in j else j, y))
                    if res[name] == {} or res[name] == []:
                        res.pop(name)
                mainthread = StoppableThread(lambda: run(res, callback))
                mainthread.start()
            elif data[0] == "STOP":
                callback({"text": "Сканирование закончено вручную", "title": "Сканирование", "color": "error"}, 1)
                mainthread.stop()
            elif data[0] == "GETSTIX":
                if pre_stix:
                    callback(pre_stix, 3)
                pre_stix = None
            elif data[0] == "POWEROFF":
                sleep(5)
                kill()
        except Exception as e:
            print(e)
    else:
        data = enc.decrypt(bytes(txt, 'utf-8', ""))
        set_cred(data)


@app.errorhandler(500)
@app.errorhandler(410)
@app.errorhandler(404)
@app.errorhandler(403)
@app.errorhandler(400)
@app.errorhandler(Exception)
def page_not_found(e):
    try:
        return render_template('error.html', res="%d - %s" % (e.code, e.name)), e.code
    except Exception as ex:
        return render_template('error.html', res=ex), ex


if __name__ == '__main__':
    server_thread = StoppableThread(lambda: app.run(port=8080, host='0.0.0.0'), start_timeout=0.2)
    server_thread.start()

    wbo_thread = StoppableThread(lambda: webbrowser.open("http://localhost:8080"), start_timeout=0.2 + 0.5)
    wbo_thread.start()

    server = WebsocketServer(9999, host='127.0.0.1', loglevel=logging.INFO)
    callback = FrontendCallBack(server)

    server.set_fn_message_received(ws_receive)
    server.run_forever()
    server_thread.stop()

    kill()
