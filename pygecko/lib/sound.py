#!/usr/bin/env python

import os


def playSound(snd):
	os.system('afplay {0!s}'.format((snd)))
