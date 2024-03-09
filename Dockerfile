# docker build -t itm:sarh-app .
# pull official base image
FROM python:3.8

# set workdir directory
WORKDIR /opt/sarh/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN  apt update && apt-get install -qy \
	locales \
	locales-all \
	libpq-dev \
	python3-dev \
	musl-dev

ENV LC_ALL es_MX.UTF-8
ENV LANG es_MX.UTF-8
ENV LANGUAGE es_MX.UTF-8

# install dependencies
RUN pip install --upgrade pip
COPY ./app/requirements.txt .
RUN pip install -r requirements.txt

