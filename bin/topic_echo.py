#!/usr/bin/env python
#
#
# copyright Kevin Walchko
#
# Basically a rostopic

from __future__ import print_function
import argparse
from pygecko.lib import TopicSub


def handleArgs():
	parser = argparse.ArgumentParser(description="""
	A simple zero MQ message tool. It will subscribe to a topic and print the messages.

	Format:
		topic_echo host port topic

	Examples:
		topic_echo 1.2.3.4 9000 cmd
	""")

	parser.add_argument('info', nargs=3, help='subscribe to messages, ex. 1.2.3.4 9000 "commands"')
	parser.add_argument('-v', '--verbose', help='display info to screen', action='store_true')
	args = vars(parser.parse_args())
	return args


def main():
	args = handleArgs()

	# check port > 8000
	# check valid host?
	host = args['info'][0]
	topic = args['info'][2]
	port = args['info'][1]

	t = TopicSub(host, port, topic)
	t.start()
	t.join()


if __name__ == '__main__':
	main()
