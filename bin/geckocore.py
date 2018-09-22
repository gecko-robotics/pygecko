#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2014 Kevin Walchko
# see LICENSE for full details
##############################################
import time
from pygecko.transport import GeckoCore


if __name__ == "__main__":
    core = GeckoCore()
    core.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
