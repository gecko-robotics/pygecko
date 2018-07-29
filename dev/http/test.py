#!/usr/bin/env python3

from time import sleep
from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    # return render_template(os.getcwd() + '/index.html')
    return render_template('index.html')

@app.route('/stream')
def stream():
    def generate():
        with open('/var/log/system.log') as f:
            while True:
                yield f.read()
                sleep(1)

    return app.response_class(generate(), mimetype='text/event-stream')

app.run()
