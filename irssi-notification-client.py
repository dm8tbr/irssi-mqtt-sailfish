#!/usr/bin/python
import sys
import time
import os
import dbus
import mosquitto

print "starting MQTT notification client!"
print "Press CTRL + C to exit"

def read_credentials_file(filename):
    f = open(filename)
    return f.readline().strip(), f.readline().strip()

mqtt_name = "sailfish_iot"
mqtt_server = "mqtt"
mqtt_port = 1883
mqtt_keepalive = 60
mqtt_credentials = os.path.expanduser("~/.mqtt_auth")
mqtt_user, mqtt_password = read_credentials_file(mqtt_credentials)
mqtt = mosquitto.Mosquitto(mqtt_name)

mqtt.username_pw_set(mqtt_user, mqtt_password)
mqtt.reconnect_delay_set(1, 300, 'true')
mqtt.connect(mqtt_server, mqtt_port, mqtt_keepalive)
mqtt.subscribe("sailfish/tbr/irssi", 0)

def on_message(mosq, obj, msg):
    print("Message received on topic "+msg.topic+" with QoS "+str(msg.qos)+" and payload "+msg.payload)
    notification = msg.payload.split('\n')
    interface.Notify("irssi",
                 0,
                 "icon-m-notifications",
                 notification[0],
                 notification[1],
                 dbus.Array(["default", ""]),
                 dbus.Dictionary({"x-nemo-preview-body": notification[1],
                             "x-nemo-preview-summary": notification[0]},
                             signature='sv'),
                 0)

mqtt.on_message = on_message

bus = dbus.SessionBus()
object = bus.get_object('org.freedesktop.Notifications','/org/freedesktop/Notifications')
interface = dbus.Interface(object,'org.freedesktop.Notifications')


while True:
        mqtt.loop()
	time.sleep(.1)

