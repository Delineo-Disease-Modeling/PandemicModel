import zlib
import base64
import json
import sys
import gc

ZIPJSON_KEY = 'base64(zip(o))'

def jsonCompress(jsonDoc):
    j = {
        ZIPJSON_KEY: base64.b64encode(
            zlib.compress(
                json.dumps(jsonDoc).encode('utf-8')
            )
        ).decode('ascii')
    }

    return j

def jsonDecompress(j, insist=True):
    try:
        assert (j[ZIPJSON_KEY])
        assert (set(j.keys()) == {ZIPJSON_KEY})
    except:
        if insist:
            raise RuntimeError("JSON not in the expected format {" + str(ZIPJSON_KEY) + ": zipstring}")
        else:
            return j

    try:
        j = zlib.decompress(base64.b64decode(j[ZIPJSON_KEY]))
    except:
        raise RuntimeError("Could not decode/unzip the contents")

    try:
        j = json.loads(j)
    except:
        raise RuntimeError("Could interpret the unzipped contents")

    return j

def get_size(obj):
    """Recursively iterate to sum size of object & members."""
    size = sys.getsizeof(obj)
    if hasattr(obj, '__iter__'):
        if hasattr(obj, 'items'):
            for key, value in obj.items():
                size += get_size(key)
                size += get_size(value)
        elif not isinstance(obj, str):
            for item in obj:
                size += get_size(item)
    return size