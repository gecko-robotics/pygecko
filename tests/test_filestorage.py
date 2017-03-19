#!/usr/bin/env python


import os
from pygecko import FileStorage


def test_yaml():
	data = {
		'bob': 1,
		'tom': 2,
		'sam': 3
	}

	fname = 'test.yaml'

	fs = FileStorage()
	fs.writeYaml(fname, data)
	fs.clear()
	fs.readYaml(fname)

	# print fs.db
	os.remove(fname)

	assert fs.db == data


def test_json():
	data = {
		'bob': 1,
		'tom': 2,
		'sam': 3
	}

	fname = 'test.json'

	fs = FileStorage()
	fs.writeJson(fname, data)
	fs.clear()
	fs.readJson(fname)

	# print fs.db
	os.remove(fname)

	assert fs.db == data
