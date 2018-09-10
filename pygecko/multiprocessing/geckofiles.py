from tempfile import NamedTemporaryFile
try:
    import simplejson as json
except ImportError:
    import json


class CoreFile(object):
    name = None
    def __init__(self, in_addr, out_addr):
        data = {'in_addr': in_addr, 'out_addr': out_addr}
        self.fd = NamedTemporaryFile(dir='/tmp', prefix='gecko', delete=True)
        self.fd.write(json.dumps(data))
        self.name = self.fd.name
        
    def __del__(self):
        self.close()
        
    def close(self):
        self.fd.close()
