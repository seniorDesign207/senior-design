import threading
import time
import RPi.GPIO as GPIO
import serial
import struct

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

ser = serial.Serial(
    port='/dev/serial0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def readSerial():
    data = ""
    while True:
        x = ser.read()
        data += x
        if x == '\r' or x == '':
            return data

def listenForSyn():
    global synRec
    global ackRec
    count = 0

    #print("listening for syn... {}".format(count))
    count += 1
    try:
        x = (ser.read()).decode()
        print("received syn: {}".format(x))
        synRec = data[0]
        ackRec = data[1]
        if synRec != 0 and ackRec == 0:
            ser.write(("{},{}\r\n".format(syn, synRec + 1)).encode())
            aligned = True

    except:
        print('error: ')

def listenForAck():
    global ackRec
    global synRec
    count = 0

    #print("Listening for ack.. {}".format(count))
    count += 1
    try:
        x = (ser.read()).decode()
        print("received ack and syn: {}".format(x))
        synRec = data[0]
        ackRec = data[1]
        if synRec != 0 and ackRec == syn + 1:
            aligned = True
    except:
        print('error: ')
                

def main():
    global synRec
    global ackRec
    global aligned
    global stopThread

    while not aligned:
        # sending syn
        str = ("{},{}\r\n".format(syn, 0)).encode()
        ser.write(str)
        tEnd = time.time() + ackWaitTime
        while time.time() < tEnd:
            # listen for ack back
            listenForAck()
        
        tEnd = time.time() + synWaitTime
        while time.time() < tEnd:
            # listen for syn
            listenForSyn()





if __name__ == "__main__":
    resetPin = 18
    syn = 1
    ackWaitTime = 2
    synWaitTime = 2
    stopThread = False
    synRec = ackRec = aligned = 0
    GPIO.setup(resetPin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(resetPin, GPIO.HIGH)

    # create send and receive thread classes and pass corresponding
    # functions to each class
    main()