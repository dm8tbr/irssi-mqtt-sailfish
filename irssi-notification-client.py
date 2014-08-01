#!/usr/bin/python
import sys
import time
import os
import string
import random
import dbus
import mosquitto

print "starting MQTT notification client!"
print "Press CTRL + C to exit"

def read_credentials_file(filename):
    f = open(filename)
    return f.readline().strip(), f.readline().strip()

def on_log(mosq, obj, level, string):
    print(string)

def on_connect(mosq, userdata, rc):
    if rc == 0:
        print("Connected to: "+mqtt_server)
        mqtt.subscribe("sailfish/tbr/irssi/notifications", 2)
        mqtt.publish("sailfish/tbr/irssi/receiver_state", "connected", 0, True)
    else:
        print("Connection failed with error code: "+rc)

mqtt_name = "sailfish_iot_"+''.join(random.choice(string.ascii_lowercase + string.digits) for i in xrange(8))
mqtt_server = "mqtt"
mqtt_port = 1883
mqtt_keepalive = 60
mqtt_credentials = os.path.expanduser("~/.mqtt_auth")
mqtt_user, mqtt_password = read_credentials_file(mqtt_credentials)
mqtt = mosquitto.Mosquitto(mqtt_name)

mqtt.username_pw_set(mqtt_user, mqtt_password)
mqtt.on_log = on_log
mqtt.on_connect = on_connect
mqtt.will_set("sailfish/tbr/irssi/receiver_state", None, 0, True)
mqtt.reconnect_delay_set(1, 300, True)
mqtt.connect(mqtt_server, mqtt_port, mqtt_keepalive)

def on_message(mosq, obj, msg):
    print("Message received on topic "+msg.topic+" with QoS "+str(msg.qos)+" and payload "+msg.payload)
    notification = msg.payload.split('\n')
    interface.Notify("irssi",
                 0,
                 "icon-m-notifications",
                 notification[0],
                 notification[1],
                 dbus.Array(["default", ""]),
                 dbus.Dictionary({"category":"x-nemo.messaging.irssi",
                             "x-nemo-preview-body": notification[1],
                             "x-nemo-preview-summary": notification[0]},
                             signature='sv'),
                 0)

mqtt.on_message = on_message

bus = dbus.SessionBus()
object = bus.get_object('org.freedesktop.Notifications','/org/freedesktop/Notifications')
interface = dbus.Interface(object,'org.freedesktop.Notifications')


mqtt.loop_forever()

