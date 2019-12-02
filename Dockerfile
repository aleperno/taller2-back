#Bla
FROM python:3.7.0-alpine

RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./* /usr/src/app/
RUN pip install -r requirements.txt
RUN python /usr/src/app/setup.py install

# copy project
COPY . /usr/src/app/
