#!/usr/bin/env python3

# put into netscan2

from __future__ import division, print_function
# import multiprocessing as mp
# import time
import bjoern
# import cv2
# import websocket
# from json2html import json2html
from jinja2 import Environment
# loader = jinja2.FileSystemLoader('./index.html')
# env = jinja2.Environment(loader=loader)
# template = env.get_template('')

# fix path for now
import sys
sys.path.append("../")


# class Camera(object):
#     def __init__(self, src):
#         self.cam = cv2.VideoCapture(src)
#
#     def read(self):
#         ret = None
#         ok, img = self.cam.read()
#         if ok:
#             img2 = cv2.resize(img, dsize=(320, 240))
#             ok, jpeg = cv2.imencode('.jpg', img2)
#             if ok:
#                 ret = jpeg.tostring()
#         return ret
#
# # urls = {'/': "hello world", '/greet': "hi user!"}
# cam = Camera(0)


def app(environ, start_response):
    print(environ)
    try:
        # response_body = urls[environ['PATH_INFO']]
        if environ['PATH_INFO'] == '/mjpeg':
            # cam = Camera(0)
            # response_body = cam.read()
            # status = '200 OK'
            # response_headers = [
            #     ('Content-Type', 'image/jpg'),
            #     ('Content-Length', str(len(response_body)))
            # ]
            # yield [response_body]
            pass
        else:
            # input = {
            #     '123.10.1.1': {'os':'linux','mac':'1234', 'last seen': '12 Jan 2018', 'open ports': '20,34,55'},
            #     '123.10.1.6': {'mac':'1236', 'last seen': '12 Jan 2018', 'open ports': '20,34,55'},
            #     '123.10.1.16': {'mac':'12364', 'last seen': '12 Jan 2018', 'open ports': '20,34,55'},
            #     '123.10.1.66': {'mac':'12636', 'last seen': '12 Jan 2018', 'open ports': '20,34,55'},
            #     'a.b.c.d': [{'a': 1}, {'a':6,'b': 3}]
            # }
            data = [
                {'ip':'123.10.1.1', 'mac':'1234', 'lastseen': '12 Jan 2018', 'openports': '20,34,55'},
                {'ip':'123.10.1.14', 'mac':'1236', 'lastseen': '12 Jan 2018', 'openports': '20,34,55'},
                {'ip':'123.10.1.13', 'mac':'12364', 'lastseen': '12 Jan 2018', 'openports': '20,34,55'},
                {'ip':'123.10.1.12', 'mac':'12636', 'lastseen': '12 Jan 2018', 'openports': '20,34,55'},
                ]

            # table = json2html.convert(json=input)

            page = """
                <!DOCTYPE html>
                <html>
                <header></header>
                <body>

                <h1>{{ title }}</h1>

                <table>
                {% for item in items %}
                <tr>
                    <td>{{item.ip}}</td>
                    <td>{{item.mac}}</td>
                    <td>{{item.openports}}</td>
                    <td>{{item.lastseen}}</td>
                </tr>
                {% endfor %}
                </table>

                </body>
                </html>
            """

            response_body = Environment().from_string(page).render(title="test", items=data).encode('utf-8')
            status = '200 OK'
            response_headers = [
                ('Content-Type', 'text/html'),
                ('Content-Length', str(len(response_body)))
            ]
            start_response(status, response_headers)
            return [response_body]

    except Exception as e:
        print(e)
        status = '404 OK'
        response_body = 'File not found'
        response_headers = [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(response_body)))
        ]
        start_response(status, response_headers)
        return [response_body]

    # print('>>', response_body)
    # start_response(status, response_headers)
    # return [response_body]
#
host = "0.0.0.0"
port = 8000
print("Starting on: {}:{}".format(host, port))
bjoern.listen(app, host, port, reuse_port=True)
bjoern.run()


# data = [
#     {'ip':'123.10.1.1', 'mac':'1234', 'lastseen': '12 Jan 2018', 'openports': '20,34,55'},
#     {'ip':'123.10.1.14', 'mac':'1236', 'lastseen': '12 Jan 2018', 'openports': '20,34,55'},
#     {'ip':'123.10.1.13', 'mac':'12364', 'lastseen': '12 Jan 2018', 'openports': '20,34,55'},
#     {'ip':'123.10.1.12', 'mac':'12636', 'lastseen': '12 Jan 2018', 'openports': '20,34,55'},
#     ]
#
# # table = json2html.convert(json=input)
#
# page = """
#     <!DOCTYPE html>
#     <html>
#     <header></header>
#     <body>
#
#     <h1>{{ title }}</h1>
#
#     <table>
#     {% for item in items %}
#     <tr>
#         <td>{{item['ip']}}</td>
#         <td>{{item.mac}}</td>
#         <td>{{item.openports}}</td>
#         <td>{{item.lastseen}}</td>
#     </tr>
#     {% endfor %}
#     </table>
#
#     </body>
#     </html>
# """
#
# response_body = Environment().from_string(page).render(title="test", items=data)
#
# print(response_body.encode('utf-8'))
