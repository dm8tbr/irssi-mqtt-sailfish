irssi-mqtt-sailfish
===================

Sailfish client for receiving (irssi) notifications over MQTT


irssi-notification-client.py
----------------------------
A quick proof of concept implementation in python. Needs python-mosquitto.
Only shows pop up and puts the notification in memory, no audio or haptic feedback.

To set up:
echo #myusername# > ~/.mqtt_auth
echo #password# > ~/.mqtt_auth

then edit the variables at the top of irssi-notification-client.py to match your environment.
