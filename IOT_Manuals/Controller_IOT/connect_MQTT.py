from Adafruit_IO import MQTTClient

import Controller_IOT.uart
from Controller_IOT.uart import *
from Controller_IOT.Helpier_Signal import *

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
def run_MQTT():
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
    global period_default
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
        if Controller_IOT.uart.state == Controller_IOT.uart.st.CONNECTED:
            Controller_IOT.uart.counter_default -= 1
            if Controller_IOT.uart.counter_default <= 0:
                Controller_IOT.uart.counter_default = period_default
                Controller_IOT.uart.state = Controller_IOT.uart.readSerial(client)

            time.sleep(Controller_IOT.uart.st.TIME_SLEEP)

# thread = threading.Thread(target=run_MQTT)
# thread.start()
# thread.join()


