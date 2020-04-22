import time

def fromDateTime(dt):
    return round(time.mktime(dt.timetuple()) + dt.microsecond/1e6)