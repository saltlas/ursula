from datetime import datetime
import json

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code. 
    currently only handles datetime objects."""

    if isinstance(obj, (datetime)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def json_serialize(data):
    return json.dumps(data, default=json_serial)    
