# Student Inputs

LAST_NAME = "SOLIS"
STUDENT_ID = "TUPM-26-1227"
SEED_NUM = int(STUDENT_ID[-1])
FAVORITE_ARTIST = "GUNS N ROSES"

ARTIST_NUMBER = len(FAVORITE_ARTIST)

s = LAST_NAME[0]
BYTEVAL = ord(s) #outputs 83

code = int(SEED_NUM * BYTEVAL / ARTIST_NUMBER)

"""Student-specific inputs and system thresholds."""

# SYSTEM SETTINGS
STREAM_LENGTH = 30        # how many readings the stream produces
SENSOR_COUNT = 4          # number of sensors in the stream
VALID_MIN = 0.0           # physically possible range (outside = invalid)
VALID_MAX = 150.0
ABNORMAL_LIMIT = 100.0    # valid reading above this = abnormal condition
CRITICAL_COUNT = 3        # abnormal conditions needed for CRITICAL status