##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
# if you don't have opencv installed and need to run a test that does
import random
import numpy as np

COLOR_BGR2GRAY = 0
COLOR_RGB2GRAY = 0
COLOR_BGR2RGB = 0
COLOR_RGB2BGR = 0

# class cvImage(object):
#     def __init__(self, w, h):
#         # I think this is a cpu hog!
#         self.img = [random.randint(0,255) for x in range(w*h)]
#         self.shape = (h,w)
#     def tobytes(self):
#         return bytes(self.img)

def cvImage(w, h, d=1):
    return np.random.randint(256, size=(d, h, w), dtype=np.uint8)


class VideoCapture(object):
    width = 1920
    height = 1080
    def __init__(self, num):
        pass

    def set(self, a, b):
        if a == 3:
            self.width = b
        elif a == 4:
            self.height = b

    def read(self):
        return True, cvImage(self.height, self.width)

    def release(self):
        pass

def cvtColor(a, b):
    return a
