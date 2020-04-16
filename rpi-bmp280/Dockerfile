# Use only for build
FROM balenalib/raspberrypi3-python:3-buster-build as build
MAINTAINER <enrique.melero@gmail.com>

# We have to build this modules, this is why we use a build base image, see later
RUN pip install Flask flask-cors jsonify smbus
RUN pip install adafruit-circuitpython-bmp280 Adafruit-Blinka 
RUN pip install RPi.GPIO

# Use slimer image for run
FROM balenalib/raspberrypi3-python:3-buster-run

# Copy the built modules from the build container
COPY --from=build ./usr/local/lib/python3.5/site-packages ./usr/local/lib/python3.5/
COPY ./src /src
CMD ["python","/src/app.py"]
#CMD ["python","/data/adafruit/examples/simpletest.py"]
