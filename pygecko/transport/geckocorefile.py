from tempfile import NamedTemporaryFile
try:
    import simplejson as json
except ImportError:
    import json


class CoreFile(object):
    def __init__(self, in_addr, out_addr, dir='/tmp'):
        prefix = 'gecko'
        data = {'in_addr': in_addr, 'out_addr': out_addr}
        self.fd = NamedTemporaryFile(dir=dir, prefix='gecko', suffix='.json', delete=True)
        self.fd.write(json.dumps(data).encode('utf8'))
        self.fd.flush()
        self.name = self.fd.name

    def __del__(self):
        self.close()

    def close(self):
        self.fd.close()
