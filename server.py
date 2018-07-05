from websocketserver import WebsocketServer
from flask import render_template, request
from flask import Flask
from Main import run
import threading
import logging
import signal
import json
import sys

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
                data['file'] = list(map(lambda x: (x[0], int(x[1]), x[2], x[3]),
                                        [i.split(';') for i in req['file_name_list'].split('\r\n')]))
            if data != {}:
                thr = threading.Thread(target=run, args=(data, callback,))
                thr.start()
        return render_template('index.html')
    except Exception as ex:
        return render_template('error.html', res=ex)


"""

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    server = WebSocketServer("localhost", 9999, WebSocket)
    server_thread = threading.Thread(target=server.listen, args=[5])
    server_thread.start()

    app.run(port=8080, host='0.0.0.0')


    def signal_handler(signal, frame):
        logging.info("Caught Ctrl+C, shutting down...")
        server.running = False
        sys.exit()


    signal.signal(signal.SIGINT, signal_handler)
"""

if __name__ == '__main__':
    def new_client(client, server):
        server.send_message_to_all("Hey all, a new client has joined us")


    server_thread = threading.Thread(target=lambda: app.run(port=8080, host='0.0.0.0'))
    server_thread.start()

    server = WebsocketServer(9999, host='127.0.0.1', loglevel=logging.INFO)
    server.set_fn_new_client(new_client)
    server.run_forever()


    def signal_handler(signal, frame):
        logging.info("Caught Ctrl+C, shutting down...")
        server.server_close()
        sys.exit()


    signal.signal(signal.SIGINT, signal_handler)
