import pickle
try:
    import simplejson as json
except ImportError:
    import json

"""
dumps -> serialize
loads -> deserialize

Ascii may have to always convert data to a string first: str(data)

For cross language (python/C/C++) you need to keep it simple and
probably just an array is best for the messages.

Pickle ------------------------------------------------------
>>> v=pickle.dumps((1,2,3,"hi"))
>>> v
b'\x80\x03(K\x01K\x02K\x03X\x02\x00\x00\x00hiq\x00tq\x01.'
>>> pickle.loads(v)
(1, 2, 3, 'hi')

Json --------------------------------------------------------
>>> v=json.dumps((1,2,3,"hi"))
>>> v
'[1, 2, 3, "hi"]'
>>> json.loads(v)
[1, 2, 3, 'hi']
"""

class Ascii(object):
    """Simple ASCII format to send info"""
    def dumps(self, data):
        return "|".join(data).encode('utf-8')
    def loads(self, msg):
        return msg.decode('utf-8').split("|")


class Json(object):
    """Use json to transport message"""
    def dumps(self, data):
        return json.dumps(data).encode('utf-8')
    def loads(self, msg):
        return json.loads(msg.decode('utf-8'))


class Pickle(object):
    """Use pickle to transport message"""
    def dumps(self, data):
        return pickle.dumps(data)
    def loads(self, msg):
        return pickle.loads(msg)
