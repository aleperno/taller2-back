#Bla
FROM ubuntu:18.04

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalo cosas de postgres
RUN apt update && apt install -y libpq-dev
RUN apt install -y python-pip

# install dependencies
RUN pip install --upgrade pip
COPY ./* /usr/src/app/
RUN pip install -r requirements.txt
RUN python /usr/src/app/setup.py install

# copy project
COPY . /usr/src/app/
