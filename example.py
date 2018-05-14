#!/usr/bin/env python

from __future__ import division, print_function
import multiprocessing as mp
import time


if __name__ == '__main__':
	print('CPU:', mp.cpu_count())

	ps = {
		# file, function, args
		'processes': [
			('camera', 'streamer', 8888,),
			('camera', 'camera_p', 0,),
			('camera', 'camera_srv', ['a', 'bunch of stuff'],),
			('camera', 'camera_srv', None,),
		]
	}

	mgr = mp.Manager()
	namespace = mgr.Namespace()
	namespace.run = True
	namespace.img_str = None

	event = mp.Event()
	event.set()

	plist = []
	for i, (mod, fun, args) in enumerate(ps['processes']):
		m = __import__(mod)
		ff = getattr(m, fun)
		if args is None:
			p = mp.Process(name=fun, target=ff, args=(namespace, event))
		else:
			p = mp.Process(name=fun, target=ff, args=(namespace, event, args))
		p.start()
		print('> Started:', mod + '.' + fun)
		plist.append(p)

	try:
		while event.is_set():
			time.sleep(1)
			# debugging info here via print or logging or webpage
	except (KeyboardInterrupt, SystemExit):
		# set the kill flag
		event.clear()

	finally:
		print('Main loop killing processes')
		for p in plist:
			p.join(timeout=1.5)
			if p.is_alive():
				print('had to kill a process:', p.name)
				p.terminate()
			else:
				print('clean exit:', p.name)
