#!/usr/bin/env python3

class cService(object):
    """
    Server calls this
    """
    def __init__(self, name, callback):
        self.name = name
        self.callback = callback
    def handle(self, req):
        # handle request/response
        # handle(request) -> response
        pass
    def shutdown(self):
        # why?
        pass
    def spin(self):
        # why??
        pass


class cServiceProxy(object):
    """
    client calls this
    """
    def __init__(self, name):
        self.name = name
    def wait_for_service(self, timeout=None):
        # this calls geckopy.wait_for_service()
        pass
    def __call__(self, *args, **kwargs):
        # ServiceProxy(1,2) -> ServiceProxy.call(1,2)
        return self.call(*args, **kwargs)
    def call(self, *args, **kwargs):
        # args is a tuple
        # kwargs is a dict
        print('-'*30)
        if args:
            print('tuple indiv', *args)
            print('tuple', args)

        if kwargs:
            print('dict', kwargs)
            print('dict keys', *kwargs)

"""
Kevin.Walchko@DFEC-4508ZK gecko $ ./funargs.py
------------------------------
tuple indiv 1 2
tuple (1, 2)
------------------------------
tuple indiv {'bob': 1, 'tom': 2}
tuple ({'bob': 1, 'tom': 2},)
------------------------------
dict {'a': 1, 'b': 2}
dict keys a b
------------------------------
dict {'bob': 1, 'tom': 2}
dict keys bob tom
"""
sp = cServiceProxy('bob')
sp(1,2)  # tuple
sp({'bob':1, 'tom':2}) # tuple
sp(a=1, b=2)  # dict
sp(**{'bob':1, 'tom':2}) # dict
