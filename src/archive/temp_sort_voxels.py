from data import DetectedObjectVoxel, Utils, compare_detected_object_voxels
#from collections import OrderedDict
from functools import cmp_to_key

raw = Utils.open_json("output.json")
d = {}
for o in raw:
    obj = DetectedObjectVoxel(o['x'],o['y'],o['z'],o['computed_range'],snr=o['snr'])
    obj.hits = o['hits']
    obj.is_object = o['is_object']
    d[obj] = obj

print(d.values())


"""
def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K
"""

print({k: v for k, v in sorted(d.items(), key=cmp_to_key(compare_detected_object_voxels))}.values())
