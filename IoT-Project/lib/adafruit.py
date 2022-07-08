from network import WLAN      # For operation of WiFi network
import time                   # Allows use of time.sleep() for delays
import pycom                  # Base library for Pycom devices
from mqtt import MQTTClient  # For use of MQTT protocol to talk to Adafruit IO
import ubinascii              # Needed to run any MicroPython code
import machine                # Interfaces with hardware components
import micropython            # Needed to run any MicroPython code
import boot

# BEGIN SETTINGS
# These need to be change to suit your environment
RANDOMS_INTERVAL = 20000 # milliseconds
last_random_sent_ticks = 0  # milliseconds


# Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "Your username"
AIO_KEY = "your aio key"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything


# FUNCTIONS

def connectAdafruit():
    pycom.heartbeat(False)
    time.sleep(0.1) # Workaround for a bug.
                    # Above line is not actioned if another
                    # process occurs immediately afterwards
    pycom.rgbled(0xff0000)  # Status red = not working


    # WIFI
    # We need to have a connection to WiFi for Internet access
    wlan = WLAN()

    while not wlan.isconnected():    # Code waits here until WiFi connects
        machine.idle()
        do_connect()
        print("was not connectd but is now Connected to Wifi")

    pycom.rgbled(0xffd7000) # Status orange: partially working

    client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)

    client.connect()

    pycom.rgbled(0x00ff00) # Status green: online to Adafruit IO
    return client

def sendDataToAdafruits(choosenfeed, value, client):
    try:
        client.publish(topic=choosenfeed, msg=str(value))
        print("Value published to feed : " + choosenfeed)
    except Exception as e:
        print("Value did not get published to feed : " + choosenfeed)
    finally:
        time.sleep(5)

def disconnectAdafruits(client):
        client.disconnect()   # ... disconnect the client and clean up.
        client = None
        wlan = WLAN()
        wlan.disconnect()
        wlan = None
        pycom.rgbled(0x000022) # Status blue: stopped
        print("Disconnected from Adafruit IO.")
