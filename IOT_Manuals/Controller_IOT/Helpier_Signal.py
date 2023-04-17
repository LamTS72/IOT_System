from enum import Enum

class Adafruit_Control:
    #username_AIO
    AIO_USERNAME = "sonlam7220"
    #key_AIO
    AIO_KEY = "aio_xGlf92dguJZ0lJMMMlcjWWkWO4T1"
    # list of IO_feed
    AIO_FEED_ID = ["button1", "button2", "sensor1", "sensor2", "sensor3", "notification", "switch_C_F"]

class Sign_Button(Enum):
    BUTTON1_OFF = '1'
    BUTTON1_ON = '2'
    BUTTON2_OFF = '3'
    BUTTON2_ON = '4'


class Sign_Payload(Enum):
    PAYLOAD_OFF = '0'
    PAYLOAD_ON = '1'

class State:
    #INIT = 0
    CONNECTED = 0
    NO_CONNECTED = 1
    MAX_ATTEMPT_CONNECT = 3
    TIME_SLEEP = 0.1 #10ms
    TIME_OVER = 30 #stick --> 3s
    TEMP_FLOOR = 5
    TEMP_HIGH = 120
    HUMI_FLOOR = 41
    HUMI_HIGH = 104


