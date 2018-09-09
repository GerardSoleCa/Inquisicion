FROM ubuntu:18.04

RUN apt-get -y update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y caffe-cpu
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python3 python-pip python3-pip python3-setuptools

COPY . /inquisicion
WORKDIR /inquisicion

RUN pip3 install -r requirements.txt && \
    python3 setup.py install

ENTRYPOINT inquisicion_bot
