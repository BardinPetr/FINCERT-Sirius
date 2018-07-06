from utils.StoppableThread import StoppableThread
from websocketserver import WebsocketServer
from flask import render_template, request
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
            if data != {}:
                thr = threading.Thread(target=run, args=(data, callback,))
                thr.start()
        return render_template('index.html')
    except Exception as ex:
        return render_template('error.html', res=ex)


if __name__ == '__main__':
    server_thread = StoppableThread(lambda: app.run(port=8080, host='0.0.0.0'))
    server_thread.start()

    server = WebsocketServer(9999, host='127.0.0.1', loglevel=logging.INFO)
    server.run_forever()
    server_thread.stop()

    os.system('kill $PPID')
