
import time

import serial.tools.list_ports
from GateWay.Helpier_Signal import *
import sys

st = State()
state = st.CONNECTED
try_times = 0
timer_counter = st.TIME_OVER
counter = 100

#search port available -> but hardcode so return specific COM
def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        #if "USB Serial Device" in strPort:
        if "Silicon Labs CP210x USB to UART Bridge" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])

    return commPort
    #return "COM8"

def detect_NoConnect_Uart(client):
    global state, try_times, timer_counter
    if(state == st.NO_CONNECTED):
        while try_times < st.MAX_ATTEMPT_CONNECT and state != st.CONNECTED:
            timer_counter -= 1
            if timer_counter <= 0 and state == st.NO_CONNECTED:
                try_times += 1
                print("Try to connect " + str(try_times) + "-time")
                state = open_Uart(client)
                timer_counter = st.TIME_OVER
            time.sleep(st.TIME_SLEEP)

            if state == st.CONNECTED:
                try_times = 0

            if try_times == st.MAX_ATTEMPT_CONNECT:
                print("No connection to UART")
                client.publish("notification", "No conntection to UART")
                sys.exit(1)
    return state

# if getPort() != "None":
#     ser = serial.Serial(port=getPort(), baudrate=115200)
#     print(ser)
def open_Uart(client):
    global ser
    #open COM and check print
    if getPort() != "None":
        try:
            ser = serial.Serial(port=getPort(), baudrate=115200)

        except:
            print("No connection to UART")
            client.publish("notification", "No connection to UART")
            return st.NO_CONNECTED

        print(ser)
        print("Connected Successfully")
        client.publish("notification", "Connected Successfully")
        return st.CONNECTED
    else:
        print("No connection to UART")
        client.publish("notification", "No connection to UART")
        return st.NO_CONNECTED

def checkSum(data):
    splitData = data.split(":")
    if len(splitData) == 5:
        checkSum_mcu = int(splitData[len(splitData) - 1].replace("#", ""))
        checkSum_data = 0
        split = 0
        for i in range(len(data)):
            if (data[i] == ":"):
                split += 1
            if split == 4:
                break
            checkSum_data += ord(data[i])
        checkSum_data += ord('#')
        if (checkSum_data == checkSum_mcu):
            return 1
        else:
            return 0

    elif len(splitData) == 2:
        if splitData[0] == '!Request':
            return 1
        elif splitData[0] == '!HELLO':
            return 1
        else:
            return 0


mess = ""
def processData(client, data):
    checksum = checkSum(data)
    if(checksum == 1):
        data = data.replace("!", "")
        data = data.replace("#", "")
        splitData = data.split(":")
        print(splitData)
        if splitData[1] == "T":
            if(float(splitData[2]) >= st.TEMP_FLOOR and float(splitData[2])  <= st.TEMP_HIGH ):
                client.publish("sensor1", splitData[2])
            else:
                client.publish("notification", "Out of range TEMPERATURE")
        elif splitData[1] == "H":
            if (float(splitData[2]) >= st.HUMI_FLOOR and float(splitData[2]) <= st.HUMI_HIGH):
                client.publish("sensor2", splitData[2])
            else:
                client.publish("notification", "Out of range HUMIDITY")
        # elif splitData[1] == "M":
        #     client.publish("sensor3", splitData[2])
        elif splitData[1] == "ERROR":
            client.publish("notification", "REQUEST ERROR")
        elif splitData[1] == "OK":
            client.publish("notification", "REQUEST OK")
        elif splitData[0] == "HELLO":
            client.publish("notification", "USER IOT SYSTEM")

    else:
        print("Data Loss")
        client.publish("notification", "Data Loss")




def readSerial(client):
    try:
        bytesToRead = ser.inWaiting()
    except:
        print("No Connection to UART")
        client.publish("notification", "No Connection to UART")
        return st.NO_CONNECTED
    #print(bytesToRead) -> number of symbols
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        print("Data from uart: " + mess)
        #print(mess) -> string message
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client, mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

    return st.CONNECTED


def writeData(data):
    return ser.write(str(data).encode())

def write2Device_Button1(payload):
    if payload == Sign_Payload['PAYLOAD_OFF'].value:
        writeData(Sign_Button['BUTTON1_OFF'].value)
    elif payload == Sign_Payload['PAYLOAD_ON'].value:
        writeData(Sign_Button['BUTTON1_ON'].value)

def write2Device_Button2(payload):
    if payload == Sign_Payload['PAYLOAD_OFF'].value:
        writeData(Sign_Button['BUTTON2_OFF'].value)
    elif payload == Sign_Payload['PAYLOAD_ON'].value:
        writeData(Sign_Button['BUTTON2_ON'].value)