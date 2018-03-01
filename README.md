# ansible-docker-python-exercise
Playing with ansible, docker and python

## 01-getweather-script <br />
Simple python script which displays weather data using https://openweathermap.org/api

Script can be run only using Python2 due to urllib2 dependency. For Python3+ use urllib, requests or pyowm as demostrated in the script.
## Usage:
```
pip install pyowm
pip install requests
```

```
export CITY_NAME="Bratislava"
export OPENWEATHER_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

printenv | grep 'CITY_NAME\|OPENWEATHER_API_KEY'
```
```
ksebesta@ksebesta-testbox:~$ printenv | grep 'CITY_NAME\|OPENWEATHER_API_KEY'
OPENWEATHER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
CITY_NAME=Bratislava
ksebesta@ksebesta-testbox:~$ 
```

```
ksebesta@ksebesta-testbox:~$ ./getweather.py 
source=openweathermap, city="Bratislava", description="light snow", temp=-6.61 degree of celsius, humidity=62.00
ksebesta@ksebesta-testbox:~$ 
```

## 02-ansible-docker-weather/ansible <br />
Run ansible playbook to install Docker; enable container logging to Docker host's syslog file; build Docker image with packed getweather.py script.

## Usage:
```
ksebesta@ksebesta-testbox:~/ansible$ sudo ansible-playbook -i "localhost," -c local docker-playbook.yml 
[sudo] password for ksebesta: 

PLAY ***************************************************************************

TASK [setup] *******************************************************************
ok: [localhost]

TASK [docker : install docker dependencies] ************************************
ok: [localhost] => (item=[u'apt-transport-https', u'ca-certificates'])

TASK [docker : add docker repo apt key] ****************************************
changed: [localhost]

TASK [docker : add Docker repository] ******************************************
changed: [localhost]

TASK [docker : install docker] *************************************************
changed: [localhost]

TASK [docker : prepare default daemon configuration] ***************************
changed: [localhost]

TASK [docker : enable docker systemd service] **********************************
ok: [localhost]

TASK [docker : build the image] ************************************************
changed: [localhost]

PLAY RECAP *********************************************************************
localhost                  : ok=8    changed=5    unreachable=0    failed=0 

```

```
ksebesta@ksebesta-testbox:~/ansible$ sudo docker run --rm -e OPENWEATHER_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" -e CITY_NAME="Bratislava" weather:dev
source=openweathermap, city="Bratislava", description="light snow", temp=-5.57 degree of celsius, humidity=57.00
ksebesta@ksebesta-testbox:~/security/ansible$ 
```

```
ksebesta@ksebesta-testbox:~/ansible$ grep openweathermap /var/log/syslog
Mar  1 16:59:55 ksebesta-testbox 57c7b6508232[11873]: source=openweathermap, city="Bratislava", description="light snow", temp=-5.57 degree of celsius, humidity=57.00
ksebesta@ksebesta-testbox:~/security/ansible$
```

## 03-network-scanner <br />
Simple scanner for repetitive network scans displaying differences between subsequent scans. Compatible both with python2 and 3 (tested on 2.7.12 & 3.5.2)

## Usage:
```
pip install python-libnmap
```

```
ksebesta@ksebesta-testbox:~$ sudo ./scanner.py --target=45.33.32.155-157 --port=22,80,389
Nmap Scan running: ETC: 0 DONE: 0%
Nmap Scan running: ETC: 1519932332 DONE: 55.56%
Nmap Scan running: ETC: 1519932333 DONE: 96.29%
Nmap Scan running: ETC: 1519932336 DONE: 100.00%
Nmap Scan running: ETC: 1519932339 DONE: 77.78%

*target - 45.33.32.155: Full Scan Results:*
TARGET              PORT         STATE         SERVICE
45.33.32.155        22/tcp       open          ssh
45.33.32.155        80/tcp       filtered      http
45.33.32.155       389/tcp       filtered      ldap
45.33.32.155        22/udp       open|filtered  ssh
45.33.32.155        80/udp       filtered      http
45.33.32.155       389/udp       open|filtered  ldap


*target - 45.33.32.156: Full Scan Results:*
TARGET              PORT         STATE         SERVICE
45.33.32.156        22/tcp       open          ssh
45.33.32.156        80/tcp       open          http
45.33.32.156       389/tcp       filtered      ldap
45.33.32.156        22/udp       open|filtered  ssh
45.33.32.156        80/udp       open|filtered  http
45.33.32.156       389/udp       open|filtered  ldap


*target - 45.33.32.157: Full Scan Results:*
TARGET              PORT         STATE         SERVICE
45.33.32.157        22/tcp       open          ssh
45.33.32.157        80/tcp       open          http
45.33.32.157       389/tcp       filtered      ldap
45.33.32.157        22/udp       filtered      ssh
45.33.32.157        80/udp       filtered      http
45.33.32.157       389/udp       filtered      ldap


Nmap done at Thu Mar  1 20:25:39 2018; 3 IP addresses (3 hosts up) scanned in 8.67 seconds
ksebesta@ksebesta-testbox:~$
```

Repetitive scan with no changes on target hosts:

```
ksebesta@ksebesta-testbox:~$ sudo ./scanner.py --target=45.33.32.155-157 --port=22,80,389
Nmap Scan running: ETC: 0 DONE: 0%
Nmap Scan running: ETC: 1519932476 DONE: 55.56%
Nmap Scan running: ETC: 1519932477 DONE: 96.30%
Nmap Scan running: ETC: 1519932479 DONE: 100.00%
Nmap Scan running: ETC: 1519932481 DONE: 77.78%
*Target - 45.33.32.155 : No new records found in the last scan.*
*Target - 45.33.32.156 : No new records found in the last scan.*
*Target - 45.33.32.157 : No new records found in the last scan.*

Nmap done at Thu Mar  1 20:28:02 2018; 3 IP addresses (3 hosts up) scanned in 8.65 seconds
ksebesta@ksebesta-testbox:~$ 
```

