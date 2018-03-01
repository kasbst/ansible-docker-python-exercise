#!/usr/bin/python

import os
import urllib2
import json
import sys

city_name = os.environ['CITY_NAME']
api_key   = os.environ['OPENWEATHER_API_KEY']


"""
 Function: get_weather_data
     Returns weather data based on provided location
     and API key. Both must be provided as environment
     variables.

 Returns:
     Weather data in a string format
"""
def get_weather_data(city_name, api_key):
    try:
       request = urllib2.Request("https://api.openweathermap.org/data/2.5/weather?q="+city_name+
                               "&APPID="+api_key+"&units=metric")
       response = urllib2.urlopen(request)
    except urllib2.URLError as e:
       print('URLError = ' + str(e.reason))
       return
    except Exception:
       import traceback
       print('generic exception: ' + traceback.format_exc())
       return


    if response.getcode() == 200:
       return response.read()
    else:
       print("HTTP: " + response.getcode() + " - getting weather data failed!")
       return

"""
 Function: parse_results
     Parse weather data to JSON format and print 
     some basic info to STDOUT

 Returns:
     Nothing
"""
def parse_results(data):
    if isinstance(data, basestring):
       try:
          parsed = json.loads(data)
       except ValueError:
          print("Parsing Weather Data has failed!")
    else:
       print("parse_results() expects string as argument!")
       return

    print('source=openweathermap, city="%s", description="%s", temp=%.2f degree of celsius, humidity=%.2f') % (
           parsed['name'], parsed['weather'][0]['description'], parsed['main']['temp'], parsed['main']['humidity'])


#######################################################
#
# Function: get_weather_with_requests
#     Just a simple demonstration how to use an external requests library
#

"""
def get_weather_with_requests(city_name, api_key):
    import requests
    r = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+city_name+
                     "&APPID="+api_key+"&units=metric")

    if r.status_code == 200:
       print('source=openweathermap, city="%s", description="%s", temp=%.2f degree of celsius, humidity=%.2f') % (
              r.json()['name'], r.json()['weather'][0]['description'], r.json()['main']['temp'], r.json()['main']['humidity'])
    else:
       print("HTTP: " + r.status_code + " - getting weather data failed!")
"""

########################################################
#
# Function: get_weather_data_with_pyowm
#     Just a simple demonstration how to use an external pyowm package
#

"""
def get_weather_data_with_pyowm(city_name, api_key):
    import pyowm
    owm = pyowm.OWM(api_key)
    observation = owm.weather_at_place(city_name)
    w = observation.get_weather()
    l = observation.get_location()
 
    print('source=openweathermap, city="%s", description="%s", temp=%s degree of celsius, humidity=%s') % (
          l.get_name(), w.get_detailed_status(), w.get_temperature(unit='celsius')['temp'], w.get_humidity())
"""

if __name__ == '__main__':
   data = get_weather_data(city_name, api_key)
   
   if data is not None:
      parse_results(data)

   #get_weather_with_requests(city_name, api_key) 
   #get_weather_data_with_pyowm(city_name, api_key)

