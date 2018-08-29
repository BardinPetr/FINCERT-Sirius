import json


class FrontendCallBack:
    def __init__(self, wsserver):
        self._ws = wsserver

    def send(self, data):
        self._ws.send_message_to_all(json.dumps(data, ensure_ascii=False))

    def log(self, logtxt):
        self.send({'xtype': 0, 'data': logtxt})

    def toast_red(self, title, text):
        self.send({'xtype': 1, "title": title, "text": text, "color": "error"})

    def toast_orange(self, title, text):
        self.send({'xtype': 1, "title": title, "text": text, "color": "warning"})

    def toast_blue(self, title, text):
        self.send({'xtype': 1, "title": title, "text": text, "color": "info"})

    def toast_green(self, title, text):
        self.send({'xtype': 1, "title": title, "text": text, "color": "success"})

    def send_results(self, data):
        res = {'xtype': 2}
        res.update(data)
        self.send(res)

    def send_running(self):
        self.send({'xtype': 4})

    def stixparse(self, data):
        res = {'xtype': 3}
        res.update(data)
        self.send(res)

    def old(self, data, cbt=0):
        res = {'xtype': cbt}
        if type(data) == dict:
            res.update(data)
        else:
            res['data'] = data
        self.send(res)
