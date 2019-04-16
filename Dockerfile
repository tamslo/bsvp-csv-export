FROM ubuntu:18.04

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# INSTALL GENERAL DEPENDENCIES

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y curl software-properties-common
RUN apt-get install -y python3-minimal virtualenv
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash
RUN apt-get install -y nodejs

# SET TIME

RUN echo Europe/Berlin >/etc/timezone
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y tzdata
RUN dpkg-reconfigure --frontend noninteractive tzdata

# INSTALL BSVP EXPORTERS FROM GIT

COPY . code
WORKDIR /code
RUN virtualenv venv -p python3
RUN source venv/bin/activate && pip install -r requirements.txt
WORKDIR /code/client
RUN npm install
