#!/usr/bin/env python

from flask import render_template, redirect, url_for, request, session
from flask import flash, Response, Flask
import bjoern
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def hello_world():
    """ serve root directory request with a static message and output to the log """

    print "This line will be output to the console log"

    # Send the response.
    resp = 'These are not the doids you are looking for... You may go. '
    return str(resp)


@socketio.on('my event')                          # Decorator to catch an event called "my event":
def test_message(message):                        # test_message() is the event callback function.
    emit('my response', {'data': 'got it!'})      # Trigger a new event called "my response"


if __name__ == "__main__":
    # if You want to use Flask's internal method to run the wsgi script you would use app.run
    # app.run(host = '0.0.0.0', port = 5000)
    # instead you want this line below
    # bjoern.run(app, '0.0.0.0', 5000, reuse_port=True)

    socketio = SocketIO(app)
    socketio.run(app)
