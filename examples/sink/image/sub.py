#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from pygecko.multiprocessing import geckopy
import cv2
# from pygecko import Image
from pygecko import msg2image
import numpy as np
import platform
import time


def subscriber(**kwargs):
    geckopy.init_node(**kwargs)

    def callback(topic, msg):
        # print('msg',msg.shape)
        # img = np.frombuffer(msg.bytes, dtype=np.uint8)
        # img = img.reshape(msg.shape)
        img = msg2image(msg)
        print('image timestamp: {:.3f}'.format(msg.timestamp))
        cv2.imshow('image',img)
        key = cv2.waitKey(1)

    geckopy.Subscriber(['camera'], callback)

    geckopy.spin(20) # it defaults to 100hz, this is just to slow it down
    print('sub bye ...')


if __name__ == '__main__':

    args = {
        'geckocore': {
            'key': 'nav'
        }
    }
    subscriber(**args)



# def callback(topic, msg):
#     img = np.frombytes(msg.d, dtype=np.uint8)
#     img.reshape(msg.shape)
#     cv2.imshow(img)
#     key = cv2.waitKey(10)


# import matplotlib.pyplot as plt
# import matplotlib.cm as colormap
# from math import sin, cos, radians
# import numpy as np
#
# class ImShow(object):
#     figsize = (5, 5)
#
#     def __init__(self, title=None):
#         fig = plt.figure(figsize=self.figsize)
#
#         # Store Python ID of figure to detect window close
#         self.figid = id(fig)
#
#         # fig.canvas.set_window_title('SLAM')
#         # plt.title(title)
#
#         self.ax = fig.gca()
#         self.ax.set_aspect("auto")
#         self.ax.set_autoscale_on(True)
#
#         # Use an "artist" to speed up map drawing
#         self.img_artist = None
#
#         # We base the axis on pixels, to support displaying the map
#         # self.ax.set_xlim([0, map_size_pixels])
#         # self.ax.set_ylim([0, map_size_pixels])
#
#         # Hence we must relabel the axis ticks to show millimeters
#         # ticks = np.arange(0,self.map_size_pixels+100,100)
#         # labels = [str(self.map_scale_mm_per_pixel * tick) for tick in ticks]
#         # self.ax.xaxis.set_ticks(ticks)
#         # self.ax.set_xticklabels(labels)
#         # self.ax.yaxis.set_ticks(ticks)
#         # self.ax.set_yticklabels(labels)
#         #
#         # self.ax.set_xlabel('X (mm)')
#         # self.ax.set_ylabel('Y (mm)')
#
#         self.ax.grid(False)
#
#     def display(self, msg):
#
#         mapimg = np.reshape(np.frombuffer(msg.bytes, dtype=np.uint8), msg.shape)
#
#         if self.img_artist is None:
#             self.img_artist = self.ax.imshow(mapimg, cmap=colormap.gray)
#         else:
#             self.img_artist.set_data(mapimg)
#
#         # If we have a new figure, something went wrong (closing figure failed)
#         if self.figid != id(plt.gcf()):
#             print("something wrong")
#             return False
#
#         # Redraw current objects without blocking
#         plt.draw()
#
#         # Refresh display, setting flag on window close or keyboard interrupt
#         ok = True
#         try:
#             plt.pause(.01) # Arbitrary pause to force redraw
#         except:
#             ok = False
#
#         return ok
#
#
# def subscriber2(**kwargs):
#     geckopy.init_node(**kwargs)
#     fig = ImShow()
#
#     def callback(topic, msg):
#         fig.display(msg)
#
#     geckopy.Subscriber(['camera'], callback)
#
#     geckopy.spin(20) # it defaults to 100hz, this is just to slow it down
#     print('sub bye ...')
