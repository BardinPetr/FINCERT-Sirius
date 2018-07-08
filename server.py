from utils.StoppableThread import StoppableThread
from utils.websocketserver import WebsocketServer
from flask import render_template, request
from utils.storage import set_cred
from flask import Flask
from Main import run
import threading
import logging
import json
import os

app = Flask(__name__)
server = None


def callback(res):
    server.send_message_to_all(json.dumps(res))


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        data = {}
        if request.method == "POST":
            req = request.form
            if 'files' in req:  # %filename%;%filesize%;%algo%;%algoresult%
                data['file'] = list(map(lambda x: (x[0], int(x[1]), {x[2]: x[3], x[4]: x[5], x[6]: x[7]}),
                                        [i.split(';') for i in req['file_name_list'].split('\r\n')]))
            if 'mail' in req:
                data['mail'] = {"email": [i.split(';') for i in req['mail_addr_list'].split('\r\n')],
                                "text": [i.split('!@<<&>>@!') for i in req['mail_txts'].split('\r\n')]}
            if data != {}:
                thr = threading.Thread(target=run, args=(data, callback,))
                thr.start()
        return render_template('index.html')
    except Exception as ex:
        return render_template('error.html', res=ex)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    try:
        data = {}
        if request.method == "POST":
            req = request.form
            set_cred({
                "cred": (req['email'], req['password']),
                "imaphost": 0,
                "imapport": 993
            })
        return render_template('settings.html')
    except Exception as ex:
        return render_template('error.html', res=ex)


if __name__ == '__main__':
    server_thread = StoppableThread(lambda: app.run(port=8080, host='0.0.0.0'))
    server_thread.start()

    server = WebsocketServer(9999, host='127.0.0.1', loglevel=logging.INFO)
    server.run_forever()
    server_thread.stop()

    os.system('kill $PPID')
