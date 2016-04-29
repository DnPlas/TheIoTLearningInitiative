#!/usr/bin/python

import paho.mqtt.client as paho
from uuid import getnode as get_mac
import psutil, signal, sys, time, dweepy
from threading import Thread

def dweeting():
    packet = dataNetwork()
    dmsg = dweepy.dweet_for(str(GetMACAddress()), {'Value': packet})
    return dmsg

def interruptHandler(signal, frame):
    sys.exit(0)

def on_publish(mosq, obj, msg):
    pass

def GetMACAddress():
    mac = get_mac()
    mac = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2)) 
    return mac

def dataNetwork():
    netdata = psutil.net_io_counters()
    return netdata.packets_sent + netdata.packets_recv

def dataNetworkHandler():
    idDevice = GetMACAddress()
    mqttclient = paho.Client()
    mqttclient.on_publish = on_publish
    mqttclient.connect("test.mosquitto.org", 1883, 60)
    while True:
        packets = dataNetwork()
        message = idDevice + " " + str(packets)
        print "dataNetworkHandler " + message
        mqttclient.publish("IoT101/idDevice/Network", message)
        time.sleep(1)

def on_message(mosq, obj, msg):
    print "MQTT dataMessageHandler %s %s" % (msg.topic, msg.payload)

def dataMessageHandler():
    mqttclient = paho.Client()
    mqttclient.on_message = on_message
    mqttclient.connect("test.mosquitto.org", 1883, 60)
    mqttclient.subscribe("IoT101/idDevice/Message", 0)
    while mqttclient.loop() == 0:
        pass

if __name__ == '__main__':

    signal.signal(signal.SIGINT, interruptHandler)

    threadx = Thread(target=dataNetworkHandler)
    threadx.start()

    threadx = Thread(target=dataMessageHandler)
    threadx.start()
    
    while True:
        dweeting()
        time.sleep(1)


# End of File
