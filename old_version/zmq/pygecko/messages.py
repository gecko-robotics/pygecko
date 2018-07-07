from collections import namedtuple
import time
import msgpack


# if i use this: use_list=False
# then do i change the below to a tuple?
def ext_pack(x):
    if x.__class__.__name__ in ['Quaternion', 'Vector', 'Pose', 'Image', 'Lidar']:
        return msgpack.ExtType(1, msgpack.packb([x.__class__.__name__,] + list(x[:]), default=ext_pack, strict_types=True))
    return x


def ext_unpack(code, data):
    if code == 1:
        # you call this again to unpack and ext_hook for nested
        d = msgpack.unpackb(data, ext_hook=ext_unpack, raw=False)

        # print d[0]   # holds class name
        # print d[1:]  # holds data inorder
        # finds constructor in namespace and calls it
        return globals()[d[0]](*d[1:])
    return msgpack.ExtType(code, data)


def serialize(msg):
    return msgpack.packb(msg, default=ext_pack, strict_types=True, use_bin_type=True)


def deserialize(data):
    return msgpack.unpackb(data, ext_hook=ext_unpack, raw=False)


def makets():
    """
    returns a timestamp
    """
    return time.time()


def formatts(ts):
    return "fixme"


# simple ones, no stamp, wouldn't just send these. They are datatypes that
# get put into a messagel
#
# cant do: func(*Vector); you would pass in timestamp too!
# but you could do: func(Vector[:3]); cut off stamp
Vector = namedtuple('Vector', 'x y z')
Quaternion = namedtuple('Quaternion', 'w x y z')

"""
OpenCV images
-------------------------------
d = img.tobytes()
s = img.shape
msg = Image(s, d, makets())

img = np.frombytes(msg.d, dtype=np.uint8)
img.reshape(msg.shape)
"""

# with timestamp
CompressedImage = namedtuple('CompressedImage', 'shape data timestamp') # jpeg compressed into bytes
Image = namedtuple('Image', 'shape data timestamp')
Lidar = namedtuple('Lidar', 'len data timestamp')
Pose = namedtuple('Pose', 'position orientation timestamp')
IMU = namedtuple('IMU', 'linear_accel angular_vel magnetic_field timestamp')
Path = namedtuple("Path", 'path')
