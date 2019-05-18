##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
# These are IntFlags, so you can compare them to ints. They
# start with 1 and go to N.
# ZmqType.pub == 1
# ZmqType.sub == 2
#
from enum import IntFlag

Status = IntFlag('Status', 'ok error topic_not_found core_not_found multiple_pub_error invalid_zmq_type')
ZmqType = IntFlag('ZmqType', 'pub sub req rep')
