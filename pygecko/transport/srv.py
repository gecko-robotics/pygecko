# from pygecko.multiprocessing.geckopy import Rate
from pygecko.multiprocessing import geckopy
from pygecko.transport.zmq_req_rep import Req



class cService(object):
    """
    Server calls this

    value?
    why not just push a Rep to srvs array?
    """
    def __init__(self, name, callback, addr):
        self.name = name
        self.callback = callback
        self.reply = Rep()
        self.reply.bind(addr)

    def handle(self):
        # handle request/response
        # handle(request) -> response
        self.reply.listen_nb(self.callback)

    # def shutdown(self):
    #     # why?
    #     pass
    # def spin(self):
    #     # why??
    #     pass


class cServiceProxy(object):
    """
    client calls this
    """
    def __init__(self, name):
        self.name = name
        self.request = Req()
        self.request.connect(addr)
    # def wait_for_service(self, timeout=None):
    #     # this calls geckopy.wait_for_service()
    #     pass
    def __call__(self, *args, **kwargs):
        # ServiceProxy(1,2) -> ServiceProxy.call(1,2)
        return self.call(*args, **kwargs)
    def call(self, *args, **kwargs):
        # args is a tuple
        # kwargs is a dict
        if kwargs:
            hz = kwargs.get('hz', 10)

        ans = None
        rate = geckopy.Rate(hz)
        while ans is None:
            ans = request.get_nb()
            rate.sleep()
        return ans
