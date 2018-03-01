# ansible-docker-python-exercise
Playing with ansible, docker and python

**01-getweather-script** <br />
Simple python script which displays weather data using https://openweathermap.org/api

Script can run only using Python2 due to urllib2 dependency. For Python3+ use urllib, requests or pyowm as demostrated in the script.
## Usage:
```
pip install pyowm
pip install requests
```

```
export CITY_NAME="Bratislava"
export OPENWEATHER_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

printenv | grep 'CITY_NAME\|OPENWEATHER_API_KEY'

ksebesta@ksebesta-testbox:~$ printenv | grep 'CITY_NAME\|OPENWEATHER_API_KEY'
OPENWEATHER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
CITY_NAME=Bratislava
ksebesta@ksebesta-testbox:~$ 
```

```
ksebesta@ksebesta-testbox:~$ ./getweather.py 
source=openweathermap, city="Bratislava", description="light snow", temp=-6.61 degree of celsius, humidity=62.00
ksebesta@ksebesta-testbox:$ 
```

**02-ansible-docker-weather/ansible** <br />

**03-network-scanner <br />
