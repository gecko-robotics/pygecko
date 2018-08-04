##############################################
# The MIT License (MIT)
# Copyright (c) 2014 Kevin Walchko
# see LICENSE for full details
##############################################
# import signal
#
#
# class SignalCatch(object):
#     """
#     Catches SIGINT and SIGTERM signals and sets kill = True
#
#     https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
#     """
#     kill = False
#     def kill_signals(self):
#         signal.signal(signal.SIGINT, self.exit_gracefully)
#         signal.signal(signal.SIGTERM, self.exit_gracefully)
#
#     def exit_gracefully(self, signum, frame):
#         """
#         When handler gets called, it sets the self.kill to True
#         """
#         self.kill = True
#         # print(">> Got signal[{}], kill = {}".format(signum, self.kill))
