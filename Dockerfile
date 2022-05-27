FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install python3-pip vim bash-completion wget libpq-dev python3-dev libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libcurl4-openssl-dev libssl-dev

RUN pip3 install virtualenv
RUN virtualenv p3
WORKDIR /p3/bin/
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN /bin/bash -c "source activate"

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED 1
COPY . /app
