import sys
import threading

from Adafruit_IO import MQTTClient
import time

import GateWay.uart
from GateWay.uart import *
from GateWay.Helpier_Signal import *

aio_sign = Adafruit_Control()

def connected(client):
    print("Connected successful ...")
    #subcribe IO-feeds in adafruit from python gateway
    for i in aio_sign.AIO_FEED_ID:
        client.subscribe(i)

def subscribe(client , userdata , mid , granted_qos):
    #notification of finish subcriber feeds to client
    print("Subscribe successful ...")

def disconnected(client):
    print("Disconnected...")
    sys.exit(1)

def message(client , feed_id , payload):
    #notification of receiving data from feeds to client
    print("Receiving data: " + payload + " from feed id: " + feed_id)
    ###############LAB3_BEGIN##################
    if feed_id == "button1":
        write2Device_Button1(payload)
    if feed_id == "button2":
        write2Device_Button2(payload)
    if feed_id == "switch_C_F":
        if payload == '0':
            a = writeData('C@')
            print(a)
        elif payload == '1':
            a = writeData('F@')
            print(a)
    ##############LAB3_END#####################
client = MQTTClient(aio_sign.AIO_USERNAME, aio_sign.AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

##############LAB1_BEGIN##################

sensor_number = 0
counter_ai = 10
prevAI_result = ""
while True:
    ##############LAB2_BEGIN###################
        # counter_ai -= 1
        # if counter_ai <= 0:
        #     counter_ai = 10
        #     nowAI_result = result_AI()
        #     if(nowAI_result != prevAI_result):
        #         prevAI_result = nowAI_result
        #         print("AI result: ", nowAI_result[2:])
        #         client.publish("ai", nowAI_result[2:])

    detect_NoConnect_Uart(client)
    if GateWay.uart.state == GateWay.uart.st.CONNECTED:
        GateWay.uart.counter -= 1
        if GateWay.uart.counter <= 0:
            GateWay.uart.counter = 100
            GateWay.uart.state = GateWay.uart.readSerial(client)

        time.sleep(GateWay.uart.st.TIME_SLEEP)

# thread = threading.Thread(target=run_MQTT)
# thread.start()
# thread.join()


