FROM python:2

ADD getweather.py /

RUN pip install pyowm
RUN pip install requests

CMD [ "python", "./getweather.py" ]
