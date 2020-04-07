# Becalm Broker
FROM resin/rpi-raspbian
MAINTAINER <blgulla@ncsu.edu>

RUN apt-get update
RUN apt-get install -y git build-essential python-dev python-smbus apt-utils i2c-tools
RUN apt-get install -y python-pip;
RUN curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
RUN python get-pip.py
RUN pip install -U pip setuptools

RUN pip install Flask flask-cors requests apscheduler

COPY ./src /src
CMD ["python","/src/app.py"]
