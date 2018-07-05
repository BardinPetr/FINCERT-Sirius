from flask import render_template, request
from flask import Flask
from Main import run
import threading

app = Flask(__name__)


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
                thr = threading.Thread(target=run, args=(data,))
                thr.start()
        return render_template('index.html')
    except Exception as ex:
        return render_template('error.html', res=ex)


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
