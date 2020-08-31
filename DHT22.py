"""
DHT22.py
Example on using DHT22 Temperature & Humidity Sensor with Adafruit library.
Based on Adafruit example code modified to contain methods to calculate Heat Index and Dew Point.
@author Adafruit (Original Example)
@author Chris Wolcott (Methods )
"""

import Adafruit_DHT
import math
import time
import sys

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN    = 16          # GPIO Pin number

humidity   = float(0.0)
temperature= float(0.0)  # Temperature in Celsius
dew_point  = float(0.0)
heat_Ndx   = float(0.0)


"""
Uses NOAA formula located at http://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml
@param  float  Air Temperature in Fahrenheit.
@param  float  Relative Humidity (0.00 - 1.00).
@return float  Heat Index in Fahrenheit.
"""

def calcHeatIndex(tmp, rH):

    # Simple Formula.  Use if Heat Index calcs to less than 80 degrees.
    heatIndex = (( 0.5 * (tmp + 61.0 + ((tmp - 68.0) * 1.2) + (rH * 0.094)) + tmp ) / 2.0)

    # Complex Formula.  Use if simple formula calcs to 80 degrees or more.
    if (heatIndex > 79.999):

        heatIndex = (-42.379 + 2.04901523 * tmp + 10.14333127 * rH - 0.22475541 * tmp * rH -
                     0.00683783 * tmp **2 - 0.05481717 * rH **2 + 0.00122874 * tmp **2 * rH +
                     0.00085282 * tmp * rH **2 - 0.00000199 * tmp **2 * rH **2)

    # Adjustments to Complex Formula result for specific temperature and humidity ranges.
        if (rH < 0.13 and tmp < 112.0):
            heatIndex = heatIndex - ((13 - rH) / 4) * math.sqrt((17 - math.abs(tmp - 95.0) / 17.0))

        if (rH > 0.85 and tmp < 87.1):
            heatIndex = heatIndex + ((rH - 85.0 / 10) * ((87.0 - tmp) / 5.0))

    return heatIndex


"""
Method to calculate temperature at which water vapor will condence from the air.  (Dew Point)
Formula taken from https://www.iothrifty.com/blogs/news/dew-point-calculator-convert-relative-humidity-to-dew-point-temperature
@param  float  Air Temperature in Celsius.
@param  float  Relative Humidity (0.00 - 1.00).
@return float  Dew Point in Celsius.
"""

def calcDewPoint(tmp, rH):

#    wrk_value = float(0.0)

    return ( (243.04 * (math.log(rH / 100) + ((17.625 * tmp) / (243.04 + tmp)))) / 17.625 -
             (math.log(rH / 100) + ((17.625 * tmp) / (243.04 + tmp))) )
#    wrk_value = (tmp * 17.27) / (237.7 + tmp) + math.log(rH / 100.0)
#    return (237.7 * wrk_value) / (17.27 - wrk_value)   [Original code, but I could not remeber where I got it.]


"""
Main program logic.
Calls Adafruit method to read DHT22 device.  Calculates Heat Index and Dew Point.
"""

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        dew_point = calcDewPoint(temperature, humidity)
        heat_Ndx  = (( calcHeatIndex(((temperature * 1.8) + 32.0), humidity) - 32.0) / 1.8)
        print ("Temp={0:0.1f}C  (Feels Like:{3:0.1f}C)  Humidity={1:0.1f}%  Dew Point={2:0.1f}C".format(temperature,humidity,dew_point,heat_Ndx))
        time.sleep(30)
    else:
        print ("Failed to retrieve data from DTH22 Sensor")

#sys.exit(0)