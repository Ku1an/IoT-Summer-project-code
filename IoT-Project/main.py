import time
import pycom
from pycoproc import Pycoproc
import machine
from machine import Pin
from SI7006A20 import SI7006A20

#Adafruit
from adafruit import sendDataToAdafruits
from adafruit import connectAdafruit
from adafruit import disconnectAdafruits



#Pysense sensor, this code is extracting de humidity data an dew piont data. A good link is https://www.weather.gov/arx/why_dewpoint_vs_humidity.
py = Pycoproc()
sensorTempHumi = SI7006A20(py)
humidity_value = round(sensorTempHumi.humidity(),2)
dew_point_value = round(sensorTempHumi.dew_point(),2)

print("Humidity value : " + str(humidity_value) + "%")
print("Dew Point value : " + str(dew_point_value))

# Temprature measurment using the MCP, analog value.
adc = machine.ADC()
temperaturepin = adc.channel(pin='P16')
millivolts = temperaturepin.voltage()
degCelsius = (millivolts - 500.0) / 10.0

# Soilmoister measurment using FCP-28, dialog value. 1 for dry , 0 for wet
pin_input = Pin('P14', mode = Pin.IN)
soilValue = pin_input.value()

if(soilValue == 1):
    soilValue = "the soil is dry! Plant need water asap"
else:
    soilValue = "the soil is perfect :D"

print("Soilmoister : " + str(soilValue))
print("Temperature : " + str(degCelsius) + " C")



## Configuring data that should be sent to Adafrutis

#All Feeds
feeds = ["somestuff"] #Change this
feed_values = [degCelsius, dew_point_value, soilValue, humidity_value]
index = 0
client = connectAdafruit()
for feed in feeds:
    sendDataToAdafruits(feed,feed_values[index],client)
    index += 1
disconnectAdafruits(client)

SLEEP_TIME = 60 #In minutes

print("pycom device going to sleep")
py.setup_sleep(SLEEP_TIME*60)
py.go_to_sleep()
