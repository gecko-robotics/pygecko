#!/usr/bin/env python

from __future__ import print_function
import argparse
import pygecko.lib.Messages as Msg
from pygecko.lib import TopicPub


def handleArgs():
	parser = argparse.ArgumentParser(description="""
	A simple zero MQ message tool. It will publish messages on a specified
	topic.

	Format:
		topic_pub port topic message -r|-once

	Examples:
		topic_pub 9000 vo -m "{'hi': 3000}" -r 10
		topic_pub 9000 vo -m "{'hi': 3000}" --once
	""")

	parser.add_argument('info', nargs=3, help='publish messages to port topic, ex. 9000 commands "{\'hi\': 3000}"')
	parser.add_argument('-v', '--verbose', help='display info to screen', action='store_true')
	parser.add_argument('-r', '--rate', help='publish rate in Hz, ex. -r 10', default=1)
	parser.add_argument('-o', '--once', help='publish a message once and exit')
	args = vars(parser.parse_args())
	return args


def main():
	args = handleArgs()

	rate = int(args['rate'])
	msg = args['info'][2]
	topic = args['info'][1]
	port = args['info'][0]

	# print(port, topic, msg)

	# clean up inputs
	if rate is None:
		rate = 1

	try:
		# json doesn't like strings with ''
		msg = msg.replace("'", '"')
		msg = Msg.deserialize(msg)  # convert string to dict

	except:
		print('Error converting your message to a dictionary for publishing ... bye')
		exit(1)

	t = TopicPub(topic, msg, rate, port)
	t.start()
	t.join()


if __name__ == '__main__':
	main()
